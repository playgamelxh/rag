package data_chunk

import (
	"github.com/tmc/langchaingo/textsplitter"
	"testing"
)

func Test_langchain(t *testing.T) {
	// 配置参数
	inputFile := "example_document.txt" // 输入文本文件
	outputDir := "recursive_chunks"     // 分片输出目录
	chunkSize := 50                     // 每个分片的目标大小（字符数）
	chunkOverlap := 20                  // 分片间重叠的字符数
	
	// 1. 加载文本内容
	text, err := LoadTextFromFile(inputFile)
	if err != nil {
		t.Fatalf("无法加载文本: %v", err)
	}
	t.Logf("成功加载文本，总长度: %d 字符\n", len(text))
	
	// 2. 初始化RecursiveCharacterTextSplitter
	// 该分片器会按以下顺序尝试分割："\n\n", "\n", " ", ""
	//splitter := textsplitter.NewRecursiveCharacterTextSplitter(
	splitter := textsplitter.NewRecursiveCharacter(
		textsplitter.WithChunkSize(chunkSize),
		textsplitter.WithChunkOverlap(chunkOverlap),
	)
	
	// 3. 执行分片
	chunks, err := splitter.SplitText(text)
	if err != nil {
		t.Fatalf("分片失败: %v", err)
	}
	
	// 4. 输出分片统计信息
	t.Logf("分片完成，共生成 %d 个分片\n", len(chunks))
	for i, chunk := range chunks {
		t.Logf("分片 %d: 长度 %d 字符\n", i+1, len(chunk))
	}
	
	// 5. 保存分片结果
	if err := SaveChunks(chunks, outputDir, inputFile); err != nil {
		t.Fatalf("保存分片失败: %v", err)
	}
	
	t.Log("所有操作完成，分片已保存到", outputDir)
}
