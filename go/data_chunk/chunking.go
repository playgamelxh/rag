package data_chunk

import (
	"fmt"
	"io/ioutil"
	"os"
	"regexp"
	"strings"
	"unicode/utf8"
)

// Chunk 表示文本分片结构，包含内容和元数据
type Chunk struct {
	Content  string   // 分片内容
	Metadata Metadata // 分片元数据
}

// Metadata 存储分片的元数据信息
type Metadata struct {
	ID             string // 分片唯一标识
	Source         string // 来源（如文件名、URL等）
	StartPos       int    // 在原始文本中的起始位置（字符索引）
	EndPos         int    // 在原始文本中的结束位置（字符索引）
	ChunkNum       int    // 当前分片序号
	TotalChunks    int    // 总分片数量
	PrevChunkID    string // 前一个分片ID，用于上下文关联
	NextChunkID    string // 后一个分片ID，用于上下文关联
	ContentType    string // 内容类型（如"plaintext", "markdown"等）
	WordCount      int    // 单词数量
	CharacterCount int    // 字符数量
}

// Chunker 定义分片器接口，所有分片策略需实现此接口
type Chunker interface {
	Chunk(text string, source string) ([]Chunk, error)
}

// -------------- 基于字符的分片器 --------------
// CharacterChunker 按字符数量进行分片，适合大多数纯文本场景
type CharacterChunker struct {
	ChunkSize    int // 每个分片的目标字符数
	ChunkOverlap int // 分片间重叠的字符数，用于保持上下文
}

// NewCharacterChunker 创建字符分片器实例
func NewCharacterChunker(chunkSize, chunkOverlap int) (*CharacterChunker, error) {
	if chunkSize <= 0 {
		return nil, fmt.Errorf("分片大小必须为正数")
	}
	if chunkOverlap < 0 || chunkOverlap >= chunkSize {
		return nil, fmt.Errorf("重叠大小必须是非负数且小于分片大小")
	}
	return &CharacterChunker{
		ChunkSize:    chunkSize,
		ChunkOverlap: chunkOverlap,
	}, nil
}

// Chunk 实现Chunker接口，执行分片操作
func (c *CharacterChunker) Chunk(text string, source string) ([]Chunk, error) {
	var chunks []Chunk
	textRunes := []rune(text)
	textLength := len(textRunes)
	start := 0
	chunkNum := 0
	
	for start < textLength {
		fmt.Println("start and textLength:", start, textLength)
		chunkNum++
		end := start + c.ChunkSize
		if end > textLength {
			end = textLength
		}
		
		// 提取分片内容
		chunkContent := string(textRunes[start:end])
		
		// 生成元数据
		chunkID := fmt.Sprintf("%s_chunk_%d", sanitizeID(source), chunkNum)
		prevChunkID := ""
		if chunkNum > 1 {
			prevChunkID = fmt.Sprintf("%s_chunk_%d", sanitizeID(source), chunkNum-1)
		}
		
		metadata := Metadata{
			ID:             chunkID,
			Source:         source,
			StartPos:       start,
			EndPos:         end,
			ChunkNum:       chunkNum,
			PrevChunkID:    prevChunkID,
			ContentType:    "plaintext",
			WordCount:      len(strings.Fields(chunkContent)),
			CharacterCount: len(chunkContent),
		}
		
		chunks = append(chunks, Chunk{
			Content:  chunkContent,
			Metadata: metadata,
		})
		
		// 计算下一个分片的起始位置，考虑重叠
		nextStart := end - c.ChunkOverlap
		minStep := 1 // 最小步进，确保每次至少前进1个字符
		nextStart = max(start+minStep, nextStart)
		
		// 同时确保 nextStart 不超过文本长度（避免越界）
		if nextStart > textLength {
			nextStart = textLength
		}
		
		start = nextStart
	}
	
	// 更新总分片数和下一个分片ID
	for i := range chunks {
		chunks[i].Metadata.TotalChunks = len(chunks)
		if i < len(chunks)-1 {
			chunks[i].Metadata.NextChunkID = chunks[i+1].Metadata.ID
		} else {
			chunks[i].Metadata.NextChunkID = ""
		}
	}
	
	return chunks, nil
}

// -------------- 基于句子的分片器 --------------
// SentenceChunker 按句子边界进行分片，保持语义完整性
type SentenceChunker struct {
	MaxChunkSize     int // 最大分片大小（字符数）
	OverlapSentences int // 重叠的句子数量
}

// NewSentenceChunker 创建句子分片器实例
func NewSentenceChunker(maxChunkSize, overlapSentences int) (*SentenceChunker, error) {
	if maxChunkSize <= 0 {
		return nil, fmt.Errorf("最大分片大小必须为正数")
	}
	if overlapSentences < 0 {
		return nil, fmt.Errorf("重叠句子数不能为负数")
	}
	return &SentenceChunker{
		MaxChunkSize:     maxChunkSize,
		OverlapSentences: overlapSentences,
	}, nil
}

// Chunk 实现Chunker接口，执行分片操作
func (s *SentenceChunker) Chunk(text string, source string) ([]Chunk, error) {
	// 预处理文本：替换换行符为空格，统一处理
	processedText := strings.ReplaceAll(text, "\n", " ")
	processedText = strings.ReplaceAll(processedText, "\r", " ")
	processedText = regexp.MustCompile(`\s+`).ReplaceAllString(processedText, " ")
	
	// 使用正则表达式分割句子（支持中英文标点）
	sentenceRegex := regexp.MustCompile(`([。！？.!?])(\s+|$)`)
	// 先在标点后添加特殊分隔符（如"||"）
	markedText := sentenceRegex.ReplaceAllString(processedText, "$1||")
	// 按特殊分隔符分割
	sentences := strings.Split(markedText, "||")
	//sentences := sentenceRegex.Split(processedText, -1)
	
	// 过滤空句子并保留标点
	var validSentences []string
	for _, sent := range sentences {
		trimmed := strings.TrimSpace(sent)
		if trimmed != "" {
			validSentences = append(validSentences, trimmed)
		}
	}
	
	if len(validSentences) == 0 {
		return []Chunk{}, nil
	}
	
	var chunks []Chunk
	currentChunk := ""
	currentSentences := []int{} // 记录当前分片中包含的句子索引
	startPos := 0
	chunkNum := 0
	i := 0
	
	for i < len(validSentences) {
		sentence := validSentences[i]
		potentialChunk := currentChunk
		if potentialChunk == "" {
			potentialChunk = sentence
		} else {
			potentialChunk += " " + sentence
		}
		
		// 检查是否超过最大长度
		if utf8.RuneCountInString(potentialChunk) <= s.MaxChunkSize {
			currentChunk = potentialChunk
			currentSentences = append(currentSentences, i)
			i++
		} else {
			// 如果当前chunk为空但句子仍然太长，强制分割
			if currentChunk == "" {
				currentChunk = substringByRune(sentence, 0, s.MaxChunkSize)
				i++
			}
			
			// 创建分片
			chunkNum++
			chunkID := fmt.Sprintf("%s_sent_chunk_%d", sanitizeID(source), chunkNum)
			prevChunkID := ""
			if chunkNum > 1 {
				prevChunkID = fmt.Sprintf("%s_sent_chunk_%d", sanitizeID(source), chunkNum-1)
			}
			
			// 计算在原始文本中的位置
			endPos := startPos + utf8.RuneCountInString(currentChunk)
			
			metadata := Metadata{
				ID:             chunkID,
				Source:         source,
				StartPos:       startPos,
				EndPos:         endPos,
				ChunkNum:       chunkNum,
				PrevChunkID:    prevChunkID,
				ContentType:    "plaintext",
				WordCount:      len(strings.Fields(currentChunk)),
				CharacterCount: len(currentChunk),
			}
			
			chunks = append(chunks, Chunk{
				Content:  currentChunk,
				Metadata: metadata,
			})
			
			// 重置当前chunk，考虑重叠
			startPos = endPos - countCharactersInSentences(validSentences,
				max(0, i-s.OverlapSentences), i)
			if startPos < 0 {
				startPos = 0
			}
			
			// 调整索引以实现句子重叠
			if s.OverlapSentences > 0 && chunkNum > 0 {
				i = max(0, i-s.OverlapSentences)
			}
			
			currentChunk = ""
			currentSentences = []int{}
		}
	}
	
	// 添加最后一个分片
	if currentChunk != "" {
		chunkNum++
		chunkID := fmt.Sprintf("%s_sent_chunk_%d", sanitizeID(source), chunkNum)
		prevChunkID := ""
		if chunkNum > 1 {
			prevChunkID = fmt.Sprintf("%s_sent_chunk_%d", sanitizeID(source), chunkNum-1)
		}
		
		endPos := startPos + utf8.RuneCountInString(currentChunk)
		
		metadata := Metadata{
			ID:             chunkID,
			Source:         source,
			StartPos:       startPos,
			EndPos:         endPos,
			ChunkNum:       chunkNum,
			PrevChunkID:    prevChunkID,
			ContentType:    "plaintext",
			WordCount:      len(strings.Fields(currentChunk)),
			CharacterCount: len(currentChunk),
		}
		
		chunks = append(chunks, Chunk{
			Content:  currentChunk,
			Metadata: metadata,
		})
	}
	
	// 更新下一个分片ID
	for i := range chunks {
		chunks[i].Metadata.TotalChunks = len(chunks)
		if i < len(chunks)-1 {
			chunks[i].Metadata.NextChunkID = chunks[i+1].Metadata.ID
		} else {
			chunks[i].Metadata.NextChunkID = ""
		}
	}
	
	return chunks, nil
}

// -------------- 基于段落的分片器 --------------
// ParagraphChunker 按段落进行分片，适合结构化文档
type ParagraphChunker struct {
	MaxChunkSize      int // 最大分片大小（字符数）
	OverlapParagraphs int // 重叠的段落数量
}

// NewParagraphChunker 创建段落分片器实例
func NewParagraphChunker(maxChunkSize, overlapParagraphs int) (*ParagraphChunker, error) {
	if maxChunkSize <= 0 {
		return nil, fmt.Errorf("最大分片大小必须为正数")
	}
	if overlapParagraphs < 0 {
		return nil, fmt.Errorf("重叠段落数不能为负数")
	}
	return &ParagraphChunker{
		MaxChunkSize:      maxChunkSize,
		OverlapParagraphs: overlapParagraphs,
	}, nil
}

// Chunk 实现Chunker接口，执行分片操作
func (p *ParagraphChunker) Chunk(text string, source string) ([]Chunk, error) {
	// 分割段落（基于空行）
	paragraphs := strings.Split(text, "\n\n")
	
	// 过滤空段落
	var validParagraphs []string
	for _, para := range paragraphs {
		trimmed := strings.TrimSpace(para)
		if trimmed != "" {
			// 替换段落内的换行符为空格
			normalized := strings.ReplaceAll(trimmed, "\n", " ")
			normalized = regexp.MustCompile(`\s+`).ReplaceAllString(normalized, " ")
			validParagraphs = append(validParagraphs, normalized)
		}
	}
	
	if len(validParagraphs) == 0 {
		return []Chunk{}, nil
	}
	
	var chunks []Chunk
	currentChunk := ""
	startPos := 0
	chunkNum := 0
	i := 0
	
	for i < len(validParagraphs) {
		para := validParagraphs[i]
		potentialChunk := currentChunk
		if potentialChunk == "" {
			potentialChunk = para
		} else {
			potentialChunk += "\n\n" + para
		}
		
		// 检查是否超过最大长度
		if utf8.RuneCountInString(potentialChunk) <= p.MaxChunkSize {
			currentChunk = potentialChunk
			i++
		} else {
			// 如果当前chunk为空但段落仍然太长，强制分割
			if currentChunk == "" {
				currentChunk = substringByRune(para, 0, p.MaxChunkSize)
				i++
			}
			
			// 创建分片
			chunkNum++
			chunkID := fmt.Sprintf("%s_para_chunk_%d", sanitizeID(source), chunkNum)
			prevChunkID := ""
			if chunkNum > 1 {
				prevChunkID = fmt.Sprintf("%s_para_chunk_%d", sanitizeID(source), chunkNum-1)
			}
			
			// 计算在原始文本中的位置
			endPos := startPos + utf8.RuneCountInString(currentChunk)
			
			metadata := Metadata{
				ID:             chunkID,
				Source:         source,
				StartPos:       startPos,
				EndPos:         endPos,
				ChunkNum:       chunkNum,
				PrevChunkID:    prevChunkID,
				ContentType:    "plaintext",
				WordCount:      len(strings.Fields(currentChunk)),
				CharacterCount: len(currentChunk),
			}
			
			chunks = append(chunks, Chunk{
				Content:  currentChunk,
				Metadata: metadata,
			})
			
			// 重置当前chunk，考虑重叠
			startPos = endPos
			
			// 调整索引以实现段落重叠
			if p.OverlapParagraphs > 0 && chunkNum > 0 {
				i = max(0, i-p.OverlapParagraphs)
			}
			
			currentChunk = ""
		}
	}
	
	// 添加最后一个分片
	if currentChunk != "" {
		chunkNum++
		chunkID := fmt.Sprintf("%s_para_chunk_%d", sanitizeID(source), chunkNum)
		prevChunkID := ""
		if chunkNum > 1 {
			prevChunkID = fmt.Sprintf("%s_para_chunk_%d", sanitizeID(source), chunkNum-1)
		}
		
		endPos := startPos + utf8.RuneCountInString(currentChunk)
		
		metadata := Metadata{
			ID:             chunkID,
			Source:         source,
			StartPos:       startPos,
			EndPos:         endPos,
			ChunkNum:       chunkNum,
			PrevChunkID:    prevChunkID,
			ContentType:    "plaintext",
			WordCount:      len(strings.Fields(currentChunk)),
			CharacterCount: len(currentChunk),
		}
		
		chunks = append(chunks, Chunk{
			Content:  currentChunk,
			Metadata: metadata,
		})
	}
	
	// 更新下一个分片ID和总分片数
	for i := range chunks {
		chunks[i].Metadata.TotalChunks = len(chunks)
		if i < len(chunks)-1 {
			chunks[i].Metadata.NextChunkID = chunks[i+1].Metadata.ID
		} else {
			chunks[i].Metadata.NextChunkID = ""
		}
	}
	
	return chunks, nil
}

// -------------- 辅助函数 --------------

// sanitizeID 将字符串处理为适合作为ID的格式
func sanitizeID(s string) string {
	// 移除特殊字符，替换为下划线
	re := regexp.MustCompile(`[^a-zA-Z0-9_]`)
	return re.ReplaceAllString(s, "_")
}

// substringByRune 按符文（rune）位置截取字符串，支持中文等多字节字符
func substringByRune(s string, start, length int) string {
	runes := []rune(s)
	if start < 0 {
		start = 0
	}
	end := start + length
	if end > len(runes) {
		end = len(runes)
	}
	if start >= end {
		return ""
	}
	return string(runes[start:end])
}

// countCharactersInSentences 计算多个句子的总字符数
func countCharactersInSentences(sentences []string, start, end int) int {
	count := 0
	for i := start; i < end && i < len(sentences); i++ {
		count += utf8.RuneCountInString(sentences[i]) + 1 // +1 是为了算上空格
	}
	return count
}

// max 返回两个整数中的最大值
func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

// -------------- 文件操作函数 --------------

// ReadTextFromFile 从文件读取文本内容
func ReadTextFromFile(filename string) (string, error) {
	content, err := ioutil.ReadFile(filename)
	if err != nil {
		return "", fmt.Errorf("读取文件失败: %v", err)
	}
	return string(content), nil
}

// WriteChunksToFiles 将分片写入文件系统
func WriteChunksToFiles(chunks []Chunk, outputDir string) error {
	// 创建输出目录
	if err := os.MkdirAll(outputDir, 0755); err != nil {
		return fmt.Errorf("创建目录失败: %v", err)
	}
	
	// 写入每个分片
	for _, chunk := range chunks {
		// 写入分片内容
		contentFilename := fmt.Sprintf("%s/%s.txt", outputDir, chunk.Metadata.ID)
		if err := ioutil.WriteFile(contentFilename, []byte(chunk.Content), 0644); err != nil {
			return fmt.Errorf("写入分片内容失败: %v", err)
		}
		
		// 写入元数据
		metaFilename := fmt.Sprintf("%s/%s_meta.txt", outputDir, chunk.Metadata.ID)
		metaContent := fmt.Sprintf(
			"ID: %s\n"+
				"Source: %s\n"+
				"Start Position: %d\n"+
				"End Position: %d\n"+
				"Chunk Number: %d/%d\n"+
				"Previous Chunk: %s\n"+
				"Next Chunk: %s\n"+
				"Content Type: %s\n"+
				"Word Count: %d\n"+
				"Character Count: %d",
			chunk.Metadata.ID,
			chunk.Metadata.Source,
			chunk.Metadata.StartPos,
			chunk.Metadata.EndPos,
			chunk.Metadata.ChunkNum,
			chunk.Metadata.TotalChunks,
			chunk.Metadata.PrevChunkID,
			chunk.Metadata.NextChunkID,
			chunk.Metadata.ContentType,
			chunk.Metadata.WordCount,
			chunk.Metadata.CharacterCount,
		)
		if err := ioutil.WriteFile(metaFilename, []byte(metaContent), 0644); err != nil {
			return fmt.Errorf("写入分片元数据失败: %v", err)
		}
	}
	
	return nil
}
