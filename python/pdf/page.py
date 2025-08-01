from PyPDF2 import PdfReader, PdfWriter

# 读取PDF文件
reader = PdfReader('1.pdf')
# 创建两个PdfWriter对象，用于保存拆分后的PDF
pdf_parts = (PdfWriter(), PdfWriter())

# 遍历PDF的每一页
for i, page in enumerate(reader.pages):
    if i < 5000:
        pdf_parts[0].add_page(page)
    else:
        pdf_parts[1].add_page(page)

# 保存前100页的PDF文件
with open('part_1.pdf', 'wb') as file1:
    pdf_parts[0].write(file1)

# 保存后部分的PDF文件
with open('part_2.pdf', 'wb') as file2:
    pdf_parts[1].write(file2)

print("PDF文件拆分完成！")