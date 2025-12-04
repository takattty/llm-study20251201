# デフォルトのMarkdownファイル
TARGET ?= slide.md

.DEFAULT_GOAL := help
.PHONY: pdf html index preview help doc doc-html build clean zip

# ドキュメント用のMarkdownファイル（slide.md以外）
DOCS := setup.md README.md

# PDFに変換するターゲット（marp用）
pdf:
	@mkdir -p pdf
	npx @marp-team/marp-cli $(TARGET) --pdf -o pdf/$(notdir $(TARGET:.md=.pdf)) --allow-local-files

# HTMLに変換するターゲット（marp用）
html:
	npx @marp-team/marp-cli $(TARGET) --html -o $(TARGET:.md=.html) --allow-local-files

index:
	npx @marp-team/marp-cli $(TARGET) --html -o index.html --allow-local-files

# プレビュー（marp用）
preview:
	npx @marp-team/marp-cli $(TARGET) --preview

# ドキュメント用MarkdownをPDFに変換（Mermaid対応）
doc:
ifndef DOC
	$(error DOC is required. Usage: make doc DOC=filename.md)
endif
	@mkdir -p pdf
	npx -p @mermaid-js/mermaid-cli mmdc -i $(DOC) -o .tmp.md -e svg
	npx md-to-pdf .tmp.md
	mv .tmp.pdf pdf/$(notdir $(DOC:.md=.pdf))
	rm -f .tmp.md .tmp-*.svg

# ドキュメント用MarkdownをHTMLに変換（Mermaid対応）
doc-html:
ifndef DOC
	$(error DOC is required. Usage: make doc-html DOC=filename.md)
endif
	@mkdir -p assets
	npx -p @mermaid-js/mermaid-cli mmdc -i $(DOC) -o .tmp_$(notdir $(DOC)) -e svg
	npx md-to-pdf --as-html --stylesheet styles/doc.css .tmp_$(notdir $(DOC))
	@mv .tmp_$(basename $(notdir $(DOC))).html $(basename $(notdir $(DOC))).html
	@if ls .tmp_$(basename $(notdir $(DOC)))-*.svg 1> /dev/null 2>&1; then \
		for svg in .tmp_$(basename $(notdir $(DOC)))-*.svg; do \
			mv "$$svg" "assets/$${svg#.tmp_}"; \
		done; \
		sed -i '' 's|src="\./.tmp_\($(basename $(notdir $(DOC)))-[0-9]*\.svg\)"|src="assets/\1"|g' $(basename $(notdir $(DOC))).html; \
	fi
	rm -f .tmp_$(notdir $(DOC))

# 全ファイルをビルド
build:
	@echo "=== Building slide.md ==="
	$(MAKE) pdf TARGET=slide.md
	$(MAKE) index TARGET=slide.md
	@echo "=== Building documents (PDF) ==="
	@for d in $(DOCS); do \
		echo "Processing $$d (PDF)..."; \
		$(MAKE) doc DOC=$$d; \
	done
	@echo "=== Building documents (HTML) ==="
	@for d in $(DOCS); do \
		echo "Processing $$d (HTML)..."; \
		$(MAKE) doc-html DOC=$$d; \
	done
	@echo "=== Converting links ==="
	@for f in index.html $(DOCS:.md=.html); do \
		sed -i '' 's|href="slide\.md"|href="index.html"|g' "$$f"; \
		sed -i '' 's|href="\./slide\.md"|href="index.html"|g' "$$f"; \
		sed -i '' 's|href="\./\([^"]*\)\.md"|href="\1.html"|g' "$$f"; \
		sed -i '' 's|href="\([^"]*\)\.md"|href="\1.html"|g' "$$f"; \
	done
	@echo "=== Creating zip ==="
	$(MAKE) zip
	@echo "=== Build complete ==="

# 不要ファイルを削除
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name ".DS_Store" -exec rm -f {} + 2>/dev/null || true
	find ./result -type f ! -name ".gitignore" -exec rm -f {} + 2>/dev/null || true

# zipファイルを作成
zip: clean
	rm -rf llm-study llm-study.zip
	mkdir llm-study
	rsync -a --exclude='.venv' --exclude='*.zip' --exclude='.git' --exclude='.DS_Store' --exclude='llm-study' . llm-study/
	zip -r llm-study.zip llm-study
	rm -rf llm-study

help:
	@echo "使い方:"
	@echo "  make build                   全ファイルをビルド"
	@echo "  make clean                   不要ファイルを削除"
	@echo "  make zip                     llm-study.zipを作成"
	@echo ""
	@echo "個別コマンド:"
	@echo "  make pdf                     $(TARGET) をPDFに変換（marp）"
	@echo "  make html                    $(TARGET) をHTMLに変換（marp）"
	@echo "  make index                   $(TARGET) をindex.htmlに変換（marp）"
	@echo "  make preview                 $(TARGET) をプレビュー（marp）"
	@echo "  make doc DOC=<file>          ドキュメントをPDFに変換"
	@echo "  make doc-html DOC=<file>     ドキュメントをHTMLに変換"
