# flext-meltano - Meltano Integration
PROJECT_NAME := flext-meltano
COV_DIR := flext_meltano
MIN_COVERAGE := 90

include ../base.mk

# === PROJECT-SPECIFIC TARGETS ===
.PHONY: test-unit test-integration build shell

.DEFAULT_GOAL := help
