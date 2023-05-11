# Product Requirements Document (PRD): Code GPT Assistant

## 1. Introduction

The purpose of this product is to create a tool that allows developers to extend the knowledge of large language models (LLMs), like ChatGPT, using content from user-provided websites and GitHub repositories. This will enable the LLM to provide up-to-date answers and solutions for niche topics in the programming domain.

## 2. Product Overview

The product will consist of a web-based interface that enables users to input URLs or GitHub repositories, which will be processed and incorporated into the LLM's knowledge base. The tool will then provide a Q&A interface for users to interact with the LLM and receive answers based on the extended knowledge.

### 2.1. Target Users

Developers who want to utilize large language models for Q&A purposes in their specific programming domains or with up-to-date information.

### 2.2. Key Features

1. User-friendly web interface to input content sources and chat with the model
2. Support for multiple input types: single URL, list of URLs, GitHub repo, or list of GitHub repos
3. Content processing pipeline that extracts, cleans, and formats data from supported sources
4. Incorporation of processed content into the LLM's knowledge base


## 3. Requirements

### 3.1. Functional Requirements

1. The tool should accept a URL, list of URLs, a GitHub repo, or list of GitHub repos as input.
2. The tool must process the content from the provided sources, supporting Markdown, HTML, and plain text formats.
3. The tool should integrate the processed content into the LLM's knowledge base.
4. The tool must provide a Q&A interface for users to interact with the LLM and receive answers based on the extended knowledge.

### 3.2. Non-functional Requirements

1. The tool must focus on English content.
2. The tool should provide clear and concise error messages in case of invalid input or processing errors.
3. The tool should be accessible through a web browser, offering compatibility with major browsers.

### 3.3. Constraints and Assumptions

1. The performance of the tool, including response time for processing content and generating answers, is not a primary concern at this stage.
2. The tool will not support languages other than English during the initial development phase.
3. Data privacy, copyright, and content licensing issues will be addressed in later iterations of the tool.