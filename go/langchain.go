package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"strings"
	
	"github.com/tmc/langchaingo/documentloaders"
	"github.com/tmc/langchaingo/embeddings"
	"github.com/tmc/langchaingo/schema"
	"github.com/tmc/langchaingo/textsplitter"
)

// 文档分块与向量的结构体（用于存储结果）
type ChunkWithVector struct {
	ChunkID    int       // 分片唯一ID
	Content    string    // 分片文本内容
	Vector     []float64 // 分片向量
	VectorDim  int       // 向量维度
	ContentLen int       // 文本长度（字符数）
}

func main() {
	// 1. 定义文档路径（确保文件存在）
	documentPath := "example_document.txt"
	if _, err := os.Stat(documentPath); os.IsNotExist(err) {
		log.Fatalf("文档不存在: %s", documentPath)
	}
	
	// 2. 加载文档
	docs, err := loadDocument(documentPath)
	if err != nil {
		log.Fatalf("加载文档失败: %v", err)
	}
	fmt.Printf("成功加载 %d 个文档\n", len(docs))
	
	// 3. 文本分块
	chunks, err := splitDocuments(docs)
	if err != nil {
		log.Fatalf("文本分块失败: %v", err)
	}
	fmt.Printf("文本分块完成，共生成 %d 个分片\n", len(chunks))
	
	// 4. 初始化嵌入模型（使用开源模型 BAAI/bge-m3）
	embedder, err := initEmbeddingModel()
	if err != nil {
		log.Fatalf("初始化嵌入模型失败: %v", err)
	}
	
	// 5. 对分块内容向量化
	chunkVectors, err := embedChunks(context.Background(), embedder, chunks)
	if err != nil {
		log.Fatalf("分块向量化失败: %v", err)
	}
	
	// 6. 输出结果示例
	printResults(chunkVectors[:3]) // 打印前3个分片的向量信息
}

// 加载文档（支持 TXT 格式，可扩展为 PDF、Markdown 等）
func loadDocument(path string) ([]schema.Document, error) {
	// 使用文本加载器加载 TXT 文件
	loader := documentloaders.NewText(path)
	return loader.Load(context.Background())
}

// 文本分块（使用递归字符分块器，适合大多数文本类型）
func splitDocuments(docs []schema.Document) ([]schema.Document, error) {
	// 配置分块参数
	splitter := textsplitter.NewRecursiveCharacterTextSplitter(
		textsplitter.WithChunkSize(300),                                          // 目标分片长度（字符）
		textsplitter.WithChunkOverlap(30),                                        // 分片重叠长度（保持上下文连贯性）
		textsplitter.WithSeparators([]string{"\n\n", "\n", ". ", ", ", " ", ""}), // 优先按换行、标点分割
	)
	
	// 执行分块
	return splitter.SplitDocuments(docs)
}

// 初始化嵌入模型（使用 HuggingFace 开源模型 BAAI/bge-m3）
func initEmbeddingModel() (embeddings.Embedder, error) {
	return embeddings.NewHuggingFaceEmbeddings(
		embeddings.WithModelName("BAAI/bge-m3"), // 模型名称
		embeddings.WithDevice("cpu"),            // 运行设备（cpu 或 cuda）
		// 可选：指定本地模型路径（若已下载）
		// embeddings.WithModelPath("./local-models/bge-m3"),
	)
}

// 对分块内容向量化
func embedChunks(ctx context.Context, embedder embeddings.Embedder, chunks []schema.Document) ([]ChunkWithVector, error) {
	var results []ChunkWithVector
	
	// 遍历所有分片，生成向量
	for i, chunk := range chunks {
		// 跳过空分片
		content := strings.TrimSpace(chunk.PageContent)
		if content == "" {
			continue
		}
		
		// 生成当前分片的向量
		vector, err := embedder.EmbedDocuments(ctx, []string{content})
		if err != nil {
			return nil, fmt.Errorf("分片 %d 向量化失败: %w", i, err)
		}
		
		// 存储结果
		results = append(results, ChunkWithVector{
			ChunkID:    i + 1,
			Content:    content,
			Vector:     vector[0], // EmbedDocuments 返回 []vector，取第一个
			VectorDim:  len(vector[0]),
			ContentLen: len(content),
		})
		
		// 打印进度（每10个分片输出一次）
		if (i+1)%10 == 0 {
			fmt.Printf("已完成 %d/%d 个分片的向量化\n", i+1, len(chunks))
		}
	}
	
	return results, nil
}

// 打印向量化结果示例
func printResults(chunkVectors []ChunkWithVector) {
	fmt.Println("\n===== 分块向量化结果示例 =====")
	for _, item := range chunkVectors {
		fmt.Printf("\n分片 ID: %d\n", item.ChunkID)
		fmt.Printf("文本长度: %d 字符\n", item.ContentLen)
		fmt.Printf("向量维度: %d\n", item.VectorDim)
		fmt.Printf("文本预览: %s...\n", truncateString(item.Content, 100))
		fmt.Printf("向量前5个值: %v...\n", item.Vector[:5]) // 仅展示前5个元素
	}
}

// 截断字符串用于预览
func truncateString(s string, maxLen int) string {
	if len(s) <= maxLen {
		return s
	}
	return s[:maxLen]
}
