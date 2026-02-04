#!/usr/bin/env python3
"""
Scrapeless Search Tool
独立的搜索工具，使用Scrapeless API进行网页抓取和搜索
"""

import json
import requests
from typing import Dict, Any

class ScrapelessSearchTool:
    """Scrapeless搜索工具类"""
    
    def __init__(self):
        self.host = "api.scrapeless.com"
        self.url = f"https://{self.host}/api/v1/unlocker/request"
        self.token = "sk_51TrByg4ezuOsAzpnNAk1UnAficirHBn4sKHpT4ZZVhT3OQAL4fELOsTjE3tCT9k"
        self.headers = {
            "x-api-token": self.token,
            "Content-Type": "application/json"
        }
    
    def search(self, query: str) -> Dict[str, Any]:
        """
        使用Scrapeless API进行搜索
        
        Args:
            query: 搜索查询或URL
            
        Returns:
            包含搜索结果的字典
        """
        try:
            # 构建请求体，使用查询作为URL或搜索词
            target_url = query if query.startswith("http") else f"https://www.google.com/search?q={query}"
            
            # 尝试不同的actor值
            actors = ["webunlocker", "unlocker.webunlocker", "unlocker"]
            
            for actor in actors:
                json_payload = {
                    "actor": actor,
                    "proxy": {
                        "country": "ANY"
                    },
                    "input": {
                        "url": target_url,
                        "method": "GET",
                        "redirect": False,
                        "jsRender": {
                            "enabled": False,
                            "headless": True,
                            "waitUntil": "domcontentloaded",
                            "instructions": [],
                            "block": {
                                "resources": [],
                                "urls": []
                            },
                            "response": {
                                "type": "html",
                                "options": {
                                    "selector": ""
                                }
                            }
                        }
                    }
                }
                
                print(f"Trying Scrapeless with actor: {actor}")
                print(f"Scrapeless request URL: {target_url}")
                
                # 发送请求
                try:
                    response = requests.post(self.url, headers=self.headers, json=json_payload, timeout=30)
                    
                    if response.status_code == 200:
                        # 解析响应
                        try:
                            result = response.json()
                            print(f"Scrapeless response received with actor {actor}: {result.get('status', 'unknown')}")
                            
                            # 提取结果
                            search_results = []
                            if "data" in result:
                                data = result["data"]
                                if "response" in data:
                                    response_data = data["response"]
                                    if "body" in response_data:
                                        body = response_data["body"]
                                        search_results.append({
                                            "title": "Scrapeless Result",
                                            "url": target_url,
                                            "content": body[:1000] + "..." if len(body) > 1000 else body
                                        })
                            
                            print(f"Found {len(search_results)} results from Scrapeless")
                            return {
                                "service": "scrapeless",
                                "query": query,
                                "results": search_results,
                                "count": len(search_results)
                            }
                        except json.JSONDecodeError:
                            print(f"Scrapeless response is not JSON for actor {actor}: {response.text}")
                            continue
                    else:
                        print(f"Scrapeless error with actor {actor}: {response.status_code} - {response.text}")
                        continue
                except Exception as e:
                    print(f"Error with actor {actor}: {str(e)}")
                    continue
            
            # 如果所有actor都失败了，返回详细的错误信息
            print("All Scrapeless actor attempts failed")
            return {
                "error": "Scrapeless API error",
                "details": "All actor attempts failed. Please check your API token and actor configuration.",
                "tried_actors": actors,
                "target_url": target_url
            }
            
        except Exception as e:
            print(f"Scrapeless search error: {str(e)}")
            return {
                "error": f"Scrapeless search error: {str(e)}"
            }

def send_request():
    """
    发送请求的示例函数
    """
    tool = ScrapelessSearchTool()
    result = tool.search("https://www.scrapeless.com")
    print("Result:", json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    send_request()
