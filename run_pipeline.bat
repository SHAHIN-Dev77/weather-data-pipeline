@echo off
cd /d D:\Data Engineer\weather-data-pipeline
call conda activate deng
python src\run_pipeline.py