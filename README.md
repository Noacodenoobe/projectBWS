# BWS + AI Ops Project - AI Orchestrator Agent

This repository houses the **AI Orchestrator Agent** for the "BWS + AI Ops" project. The agent's primary role is to analyze project files, construct coherent task sets, identify inconsistencies, manage a knowledge base, and automate GitHub Project workflows.

## Project Scopes

The project is divided into two main scopes, managed in parallel:

### [A] AI-Ops (AI Operations for GitHub)
This scope focuses on the assistant's architecture, prompts, automations, workflows, and GitHub Actions related to working with GitHub.

### [B] BWS (Greenery Project)
This scope covers the specific greenery project details, including walls/suspensions/islands/planters, logistics, Bill of Materials (BOM), and scheduling.

## Repository Structure

- `kb/`: Knowledge Base - Contains structured information about the project (e.g., `ops_model.md`, `bws_project.md`, `dictionary.md`, `file_map.csv`).
- `prompts/`: AI Prompts - Stores various prompts used by the AI agents.
- `files/src/`: Source Code - Python scripts and other code for automation and data processing.
- `docs/`: Documentation - General project documentation, including converted binary files (`_converted/`).

## Important Note: Tesseract OCR Requirement

For the AI Orchestrator Agent to fully process all project files, especially PDF and PNG documents, **Tesseract OCR must be installed on your operating system**. Without it, the agent cannot extract text from these image-based files, which will result in incomplete information in the knowledge base.

Instructions for installing Tesseract OCR can be found in `requirements.txt`.

## Getting Started

1.  **Install Python Dependencies**: Ensure all required Python libraries are installed by running `pip install -r requirements.txt`.
2.  **(Critical) Install Tesseract OCR**: Follow the instructions in `requirements.txt` to install Tesseract OCR on your system.
3.  **Review the Knowledge Base**: Start by exploring the [Knowledge Base Index](kb/index.md) for a comprehensive understanding of the project.
4.  **GitHub Project Setup**: The agent is designed to automate GitHub Project setup, including creating repositories, issues, and labels. Refer to `README_GITHUB_PROJECT_GUIDE.md` for more details.

## Further Information

- **Project Master Prompt**: See `promptMASTER.md` for the core instructions guiding the AI Orchestrator Agent.
- **AI-Ops Model Details**: Refer to `kb/ops_model.md` for a deep dive into the agent's architecture, rules, memory, and tools.