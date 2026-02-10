[English](README.md) | [繁體中文](README.zh.md)

# create-skill

一個 Claude Code 技能，引導使用者根據需求建立新的 Claude Code 技能。

## 說明

此技能將使用者的描述轉化為結構完整的 Claude Code 技能。它會完整執行技能建立流程：收集需求、規劃檔案結構、撰寫含有正確 frontmatter 的 SKILL.md、建立輔助資源（參考文件、範例、腳本），以及驗證成果。

## 功能特色

- 透過針對性的問題來理解技能的用途和觸發情境
- 決定適當的結構（精簡型、標準型或完整型）
- 產生含有效 YAML frontmatter 和祈使語氣內文的 SKILL.md
- 建立輔助檔案：參考文件、可執行範例、工具腳本和資產範本
- 根據完整檢查清單驗證最終技能
- 涵蓋常見模式：知識/指南型、自動化型、範本產生型、CLI 封裝型和純使用者呼叫型

## 安裝

將技能目錄複製到 Claude Code 技能資料夾：

```
cp -r create-skill ~/.claude/skills/
```

放置在 `~/.claude/skills/` 的技能會被 Claude Code 自動發現，無需額外註冊。

## 使用方式

透過要求 Claude Code 建立技能來觸發此技能。範例提示：

- 「建立一個用於 Docker 部署的技能」
- 「製作一個幫助撰寫單元測試的新技能」
- 「建立一個程式碼審查標準的技能」
- 「產生一個 API 端點架構的技能範本」

Claude 會自動執行需求收集、規劃、撰寫和驗證等階段。
