import os, sys
import logging, logging.config

# rouuter에서 작동되는 로그는 각각 파일에 맞는 디렉토리를 생성 후 진행해야한다.
def logger_type(logger_type):
    
    logging.config.fileConfig('./config/logging.conf')
    
    return logging.getLogger(logger_type)