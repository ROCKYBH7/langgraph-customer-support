# mcp_concept.py - Step 5: Understanding MCP (Model Context Protocol)

"""
MCP CONCEPT EXPLANATION:

Think of MCP like having two different assistants:

1. COMMON Assistant 🔷 - Does internal tasks (no internet needed)
   - Text parsing, calculations, formatting
   - Like having a smart calculator/text processor

2. ATLAS Assistant 🔶 - Does external tasks (needs internet/databases)
   - Looking up customer data, sending emails, API calls
   - Like having someone who can call other companies for you

Your agent decides which assistant to use for each task!
"""

import asyncio
import logging
from enum import Enum
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPServer(Enum):
    COMMON = "common"  # Internal processing
    ATLAS = "atlas"    # External systems

class MockMCPClient:
    """
    This simulates what a real MCP client would do
    In reality, this would connect to actual servers
    """
    
    def __init__(self, server_type: MCPServer):
        self.server_type = server_type
        logger.info(f"🔗 Connected to {server_type.value.upper()} server")
    
    async def execute_ability(self, ability_name: str, data: Dict) -> Dict[str, Any]:
        """Execute an ability on this server"""
        logger.info(f"📡 Executing '{ability_name}' on {self.server_type.value.upper()} server")
        
        # Simulate different processing based on server type
        if self.server_type == MCPServer.COMMON:
            return await self._handle_common_ability(ability_name, data)
        else:  # ATLAS
            return await self._handle_atlas_ability(ability_name, data)
    
    async def _handle_common_ability(self, ability: str, data: Dict) -> Dict:
        """Handle COMMON server abilities - internal processing only"""
        # Simulate some processing time
        await asyncio.sleep(0.1)
        
        if ability == "parse_request_text":
            return {
                "structured_data": {
                    "intent": "billing_issue" if "billing" in data.get("query", "").lower() else "general",
                    "sentiment": "frustrated" if "!" in data.get("query", "") else "neutral",
                    "processed_by": "COMMON_SERVER"
                }
            }
        elif ability == "solution_evaluation":
            return {
                "scores": [
                    {"solution": "automated_fix", "score": 92},
                    {"solution": "manual_review", "score": 78},
                    {"solution": "escalate", "score": 65}
                ],
                "processed_by": "COMMON_SERVER"
            }
        elif ability == "response_generation":
            return {
                "response": f"Thank you {data.get('customer_name', 'Customer')}. I've processed your request.",
                "processed_by": "COMMON_SERVER"
            }
        else:
            return {"result": f"COMMON server processed: {ability}", "processed_by": "COMMON_SERVER"}
    
    async def _handle_atlas_ability(self, ability: str, data: Dict) -> Dict:
        """Handle ATLAS server abilities - external system integration"""
        # Simulate external API calls (longer processing time)
        await asyncio.sleep(0.3)
        
        if ability == "extract_entities":
            return {
                "entities": {
                    "customer_id": "CUST_12345",
                    "product": "Premium Plan",
                    "account_status": "active",
                    "last_payment": "2024-01-15"
                },
                "processed_by": "ATLAS_SERVER"
            }
        elif ability == "knowledge_base_search":
            return {
                "articles": [
                    {"title": "Billing FAQ", "relevance": 0.92, "url": "kb/billing-faq"},
                    {"title": "Refund Policy", "relevance": 0.85, "url": "kb/refunds"}
                ],
                "processed_by": "ATLAS_SERVER"
            }
        elif ability == "update_ticket":
            return {
                "ticket_updated": True,
                "new_status": "in_progress",
                "assigned_agent": data.get("escalate", False) and "human_agent_001" or "ai_agent",
                "processed_by": "ATLAS_SERVER"
            }
        else:
            return {"result": f"ATLAS server processed: {ability}", "processed_by": "ATLAS_SERVER"}

class MCPOrchestrator:
    """
    This decides which server to use for each ability
    Think of this as a smart dispatcher
    """
    
    def __init__(self):
        self.common_client = MockMCPClient(MCPServer.COMMON)
        self.atlas_client = MockMCPClient(MCPServer.ATLAS)
        
        # Define which abilities go to which server
        self.ability_routing = {
            # COMMON server - internal processing
            "parse_request_text": MCPServer.COMMON,
            "normalize_fields": MCPServer.COMMON,
            "add_flags_calculations": MCPServer.COMMON,
            "solution_evaluation": MCPServer.COMMON,
            "response_generation": MCPServer.COMMON,
            
            # ATLAS server - external systems
            "extract_entities": MCPServer.ATLAS,
            "enrich_records": MCPServer.ATLAS,
            "clarify_question": MCPServer.ATLAS,
            "knowledge_base_search": MCPServer.ATLAS,
            "escalation_decision": MCPServer.ATLAS,
            "update_ticket": MCPServer.ATLAS,
            "execute_api_calls": MCPServer.ATLAS,
            "trigger_notifications": MCPServer.ATLAS
        }
    
    async def execute_ability(self, ability_name: str, data: Dict) -> Dict[str, Any]:
        """Route ability to correct server and execute"""
        server_type = self.ability_routing.get(ability_name)
        
        if not server_type:
            logger.warning(f"⚠️ Unknown ability: {ability_name}")
            return {"error": "Unknown ability"}
        
        logger.info(f"🎯 Routing '{ability_name}' to {server_type.value.upper()} server")
        
        if server_type == MCPServer.COMMON:
            return await self.common_client.execute_ability(ability_name, data)
        else:
            return await self.atlas_client.execute_ability(ability_name, data)

# Demo: Understanding MCP routing
async def demo_mcp_concept():
    logger.info("🚀 MCP Concept Demo - Understanding Server Routing")
    
    orchestrator = MCPOrchestrator()
    
    # Sample customer data
    customer_data = {
        "customer_name": "Bob Smith",
        "query": "I need help with my billing!",
        "ticket_id": "TKT-002"
    }
    
    # Test different abilities and see which server they go to
    test_abilities = [
        "parse_request_text",      # Should go to COMMON
        "extract_entities",        # Should go to ATLAS
        "solution_evaluation",     # Should go to COMMON
        "knowledge_base_search",   # Should go to ATLAS
        "response_generation"      # Should go to COMMON
    ]
    
    logger.info("\n📊 ROUTING DEMONSTRATION:")
    
    for ability in test_abilities:
        logger.info(f"\n--- Testing: {ability} ---")
        result = await orchestrator.execute_ability(ability, customer_data)
        logger.info(f"✅ Result: {result.get('processed_by', 'Unknown server')}")
    
    logger.info("\n🎓 LESSON LEARNED:")
    logger.info("🔷 COMMON server = Internal processing (parsing, calculations)")
    logger.info("🔶 ATLAS server = External systems (databases, APIs, notifications)")
    logger.info("🎯 The orchestrator automatically routes each ability to the right server!")

if __name__ == "__main__":
    asyncio.run(demo_mcp_concept())