package data_chunk

import (
	"context"
	"fmt"
	"os"
	"strings"
	
	"github.com/tmc/langchaingo/documentloaders"
)

// 保存分片结果到文件
func SaveChunks(chunks []string, outputDir string, source string) error {
	// 创建输出目录
	if err := os.MkdirAll(outputDir, 0755); err != nil {
		return fmt.Errorf("创建目录失败: %v", err)
	}
	
	// 保存每个分片
	for i, chunk := range chunks {
		filename := fmt.Sprintf("%s/%s_chunk_%d.txt", outputDir, SanitizeFilename(source), i+1)
		if err := os.WriteFile(filename, []byte(chunk), 0644); err != nil {
			return fmt.Errorf("写入分片 %d 失败: %v", i+1, err)
		}
		fmt.Printf("已保存分片 %d: %s\n", i+1, filename)
	}
	
	return nil
}

// 清理文件名，移除特殊字符
func SanitizeFilename(name string) string {
	// 替换路径分隔符和特殊字符
	name = strings.ReplaceAll(name, "/", "_")
	name = strings.ReplaceAll(name, "\\", "_")
	name = strings.ReplaceAll(name, ":", "_")
	name = strings.ReplaceAll(name, "*", "_")
	name = strings.ReplaceAll(name, "?", "_")
	name = strings.ReplaceAll(name, "\"", "_")
	name = strings.ReplaceAll(name, "<", "_")
	name = strings.ReplaceAll(name, ">", "_")
	name = strings.ReplaceAll(name, "|", "_")
	return name
}

// 从文件加载文本
func LoadTextFromFile(filename string) (string, error) {
	// 1. 先打开文件获取io.Reader
	file, err := os.Open(filename)
	if err != nil {
		return "", fmt.Errorf("无法打开文件: %v", err)
	}
	defer file.Close() // 确保文件会被关闭
	
	// 使用LangChain的文件加载器
	loader := documentloaders.NewText(file)
	docs, err := loader.Load(context.Background())
	if err != nil {
		return "", fmt.Errorf("加载文件失败: %v", err)
	}
	
	if len(docs) == 0 {
		return "", fmt.Errorf("文件中没有内容")
	}
	
	return docs[0].PageContent, nil
}
