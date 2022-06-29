# -*- coding: utf-8 -*-
"""
    pythonで書かれた関数を、web上でやり取りするためのAPIサーバを構築するためのスクリプト
    (C) Masayuki Kanai 2022/02/22
"""


import os
import sys
import json
import re
import datetime
import uvicorn
import configparser

from fastapi import FastAPI, Request, Query, Path, Body, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from project_logger import ProjectLogger

"""AIスクリプトのimport"""
from ai_script.sample_script import sample_func as SampFunc

"""FastAPIの設定"""
tags_metadata = [
    {"name": "SampFunc", "description": "サンプルスクリプト"},
]
app = FastAPI(
        title='Simple API',
        description= 'Simple API',
        version='1.00',
        openapi_tags=tags_metadata
        )

logger = ProjectLogger("/data/project/log/api.log")

message_ini = configparser.ConfigParser()
message_ini.read('/data/project/message.ini', 'UTF-8')

class ApiException(Exception):
    def __init__(self, endpoint: str, error_code: int, message: str):
        self.endpoint = endpoint
        self.error_code = error_code
        self.message = message

@app.on_event("startup")
async def startup_event():
    info_log("Simple API startup")
    if not message_ini.sections():
        error_log("message_ini is invalid data.")
    if not message_ini.has_section('project1'):
        error_log("message_ini has not project1 section.")
    if not message_ini.has_section('project1'):
        error_log("message_ini has not project2 section.")

@app.on_event("shutdown")
async def shutdown_event():
    info_log("Simple API shutdown")

@app.middleware("http")
async def logging_requested_from(request: Request, call_next):
    if request.headers.get('x-amzn-trace-id') is None:
        return await call_next(request)
    if not re.match('^(/api/)+([A-Za-z0-9_\-])', request.url.path):
        return await call_next(request)        
    info_log("Start API HTTP Request process: amzn-trace-id=%s. url=%s" % (request.headers['x-amzn-trace-id'], request.url))
    response = await call_next(request)
    info_log("API HTTP Request process Finished: amzn-trace-id=%s ip-address=%s" % (request.headers['x-amzn-trace-id'], request.headers['x-forwarded-for']))
    return response

# ApiExceptionをキャッチする。
@app.exception_handler(ApiException)
async def api_exception_handler(request: Request, exc: ApiException):
    error_log("API Error: endpoint=%s message=%s" % (exc.endpoint, exc.message))
    message = None
    try:
        message = message_ini.get(exc.endpoint, 'status%s' % exc.error_code)
    except Exception as ex:
        message = exc.message    
    return JSONResponse(status_code=500, content={"status": exc.error_code, "message": message, "version": app.version})

@app.get("/")
async def index():
    """死活監視"""
    return "OK"

@app.get("/api/test")
async def test(request: Request):
    return {
        "headers": request.headers
    }

@app.post("/api/ai_script", tags=["AI_SCRIPT"])
async def ai_script(json_data=Body(...)):
    """AI_Script呼び出し"""
    error_code = 999
    message = "something wrong."
    try:
        if not any(json_data):
            raise HTTPException(status_code=400, detail="requested json data is empty.")
        """AI実行"""
        info_log("Starting AI:ai_script now... params=%s" % json_data)
        status, message = SampFunc(json_data)
        if status != 200:
            raise HTTPException(status_code=500, detail="exec ai failed. accept no is not published. ")
        return {"status": status, "version": app.version, "message": message}
    except HTTPException as ex:
        error_code = ex.status_code
        message = ex.detail
    except Exception as ex:
        error_log("Error ai_script: %s" % ex)
    raise ApiException(endpoint=sys._getframe().f_code.co_name, error_code=error_code, message=message)

def info_log(msg=''):
    if logger is None:
        return
    logger.info('[%s] %s' % ("SimpleAPI", msg))

def warning_log(msg=''):
    if logger is None:
        return
    logger.warn('[%s] %s' % ("SimpleAPI", msg))

def error_log(msg=''):
    if logger is None:
        return
    logger.error('[%s] %s' % ("SimpleAPI", msg))

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080, headers=[("server", "HEROZ/API Server for SimpleAPI")])