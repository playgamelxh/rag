package data_chunk

import (
	"testing"
	"unicode/utf8"
)

// -------------- 主函数示例 --------------
func Test_data_chunking(t *testing.T) {
	// 配置参数
	inputFile := "example_document.txt" // 输入文档
	outputDir := "chunk_output"         // 分片输出目录
	characterChunkSize := 1000          // 字符分片大小
	characterOverlap := 100             // 字符分片重叠
	sentenceMaxSize := 1500             // 句子分片最大大小
	sentenceOverlap := 1                // 句子分片重叠
	paragraphMaxSize := 3000            // 段落分片最大大小
	paragraphOverlap := 0               // 段落分片重叠
	
	// 读取输入文档
	text, err := ReadTextFromFile(inputFile)
	if err != nil {
		t.Fatalf("无法读取输入文件: %v", err)
	}
	t.Logf("成功读取文档，共 %d 个字符\n", utf8.RuneCountInString(text))
	
	// 初始化不同的分片器
	charChunker, err := NewCharacterChunker(characterChunkSize, characterOverlap)
	if err != nil {
		t.Fatalf("初始化字符分片器失败: %v", err)
	}
	
	sentChunker, err := NewSentenceChunker(sentenceMaxSize, sentenceOverlap)
	if err != nil {
		t.Fatalf("初始化句子分片器失败: %v", err)
	}
	
	paraChunker, err := NewParagraphChunker(paragraphMaxSize, paragraphOverlap)
	if err != nil {
		t.Fatalf("初始化段落分片器失败: %v", err)
	}
	
	// 执行分片
	t.Log("开始执行字符分片...")
	charChunks, err := charChunker.Chunk(text, inputFile)
	if err != nil {
		t.Fatalf("字符分片失败: %v", err)
	}
	t.Logf("字符分片完成，生成 %d 个分片\n", len(charChunks))
	
	t.Log("开始执行句子分片...")
	sentChunks, err := sentChunker.Chunk(text, inputFile)
	if err != nil {
		t.Fatalf("句子分片失败: %v", err)
	}
	t.Logf("句子分片完成，生成 %d 个分片\n", len(sentChunks))
	
	t.Log("开始执行段落分片...")
	paraChunks, err := paraChunker.Chunk(text, inputFile)
	if err != nil {
		t.Fatalf("段落分片失败: %v", err)
	}
	t.Logf("段落分片完成，生成 %d 个分片\n", len(paraChunks))
	
	// 保存分片结果
	t.Log("正在保存分片结果...")
	if err := WriteChunksToFiles(charChunks, outputDir+"/character_based"); err != nil {
		t.Fatalf("保存字符分片失败: %v", err)
	}
	
	if err := WriteChunksToFiles(sentChunks, outputDir+"/sentence_based"); err != nil {
		t.Fatalf("保存句子分片失败: %v", err)
	}
	
	if err := WriteChunksToFiles(paraChunks, outputDir+"/paragraph_based"); err != nil {
		t.Fatalf("保存段落分片失败: %v", err)
	}
	
	t.Log("所有分片操作已完成，结果保存在", outputDir)
	
	t.Log("over!")
}
