# flext-meltano - Meltano Integration
PROJECT_NAME := flext-meltano
include ../base.mk

# === PROJECT-SPECIFIC TARGETS ===
.PHONY: test-unit test-integration build shell

.DEFAULT_GOAL := help
