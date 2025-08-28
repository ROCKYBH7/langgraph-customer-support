# full_langgraph_agent.py -  Complete Implementation

"""
This is the COMPLETE LangGraph Customer Support Agent
Now you understand:
1. ✅ How data flows between stages (CustomerSupportPayload)
2. ✅ How stages make decisions (deterministic vs non-deterministic)  
3. ✅ How MCP routing works (COMMON vs ATLAS servers)

Let's put it all together for the full 11-stage workflow!
"""

import asyncio
import json
import logging
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, Any, List, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

class StageMode(Enum):
    DETERMINISTIC = "deterministic"          # Execute abilities in order
    NON_DETERMINISTIC = "non_deterministic"  # Dynamic decision making
    HUMAN_INTERACTION = "human_interaction"  # Wait for human input

class MCPServer(Enum):
    COMMON = "common"  # Internal processing
    ATLAS = "atlas"    # External systems

@dataclass
class CustomerSupportPayload:
    """The 'state' that travels through all 11 stages"""
    # Input data
    customer_name: str
    email: str
    query: str
    priority: str
    ticket_id: str
    
    # Stage results (populated as we go)
    parsed_data: Optional[Dict] = None
    extracted_entities: Optional[Dict] = None
    normalized_fields: Optional[Dict] = None
    enriched_records: Optional[Dict] = None
    flags_calculations: Optional[Dict] = None
    clarification_needed: Optional[bool] = None
    clarification_answer: Optional[str] = None
    knowledge_base_results: Optional[List] = None
    solution_scores: Optional[List] = None
    escalation_decision: Optional[bool] = None
    ticket_updates: Optional[Dict] = None
    generated_response: Optional[str] = None
    api_results: Optional[Dict] = None
    notifications_sent: Optional[List] = None
    
    # Tracking
    stage_history: List[str] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.stage_history is None:
            self.stage_history = []
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

# ═══════════════════════════════════════════════════════════════════════════════
# MCP CLIENT SIMULATION
# ═══════════════════════════════════════════════════════════════════════════════

class MockMCPClient:
    def __init__(self, server_type: MCPServer):
        self.server_type = server_type
    
    async def execute_ability(self, ability_name: str, payload: CustomerSupportPayload) -> Dict[str, Any]:
        logger.info(f"📡 {ability_name} → {self.server_type.value.upper()} server")
        await asyncio.sleep(0.1)  # Simulate processing time
        
        # Mock responses based on ability
        responses = {
            # COMMON server abilities
            "parse_request_text": {"intent": "billing_issue", "sentiment": "frustrated"},
            "normalize_fields": {"date_format": "ISO", "priority_code": payload.priority},
            "add_flags_calculations": {"sla_risk": "medium", "priority_score": 85},
            "solution_evaluation": {
                "scores": [
                    {"solution": "automated_refund", "score": 95},
                    {"solution": "manual_review", "score": 75}
                ]
            },
            "response_generation": {
                "response": f"Dear {payload.customer_name}, thank you for contacting us. Your issue has been resolved."
            },
            
            # ATLAS server abilities  
            "extract_entities": {"product": "Premium Plan", "account_id": "ACC-123"},
            "enrich_records": {"sla_hours": 24, "previous_tickets": 2},
            "clarify_question": {"question": "Can you provide your account number?"},
            "extract_answer": {"answer": "My account number is ACC-789"},
            "knowledge_base_search": {"articles": [{"title": "Billing FAQ", "relevance": 0.92}]},
            "escalation_decision": {"escalate": False, "confidence": 0.95},
            "update_ticket": {"status": "resolved", "resolution_time": "45min"},
            "close_ticket": {"closed": True, "satisfaction_survey_sent": True},
            "execute_api_calls": {"refund_processed": "$25.00", "api_calls": 3},
            "trigger_notifications": {"email_sent": True, "sms_sent": False}
        }
        
        return responses.get(ability_name, {"result": f"Mock result for {ability_name}"})

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN LANGGRAPH AGENT
# ═══════════════════════════════════════════════════════════════════════════════

class LangGraphCustomerSupportAgent:
    """
    The complete 11-stage customer support agent
    """
    
    def __init__(self):
        self.common_client = MockMCPClient(MCPServer.COMMON)
        self.atlas_client = MockMCPClient(MCPServer.ATLAS)
        
        # Stage configuration - this is the "graph" definition
        self.stage_config = {
            "INTAKE": {
                "mode": StageMode.DETERMINISTIC,
                "abilities": [],  # Just accept payload
                "description": "📥 Accept customer request"
            },
            "UNDERSTAND": {
                "mode": StageMode.DETERMINISTIC,
                "abilities": [
                    {"name": "parse_request_text", "server": MCPServer.COMMON},
                    {"name": "extract_entities", "server": MCPServer.ATLAS}
                ],
                "description": "🧠 Parse and understand request"
            },
            "PREPARE": {
                "mode": StageMode.DETERMINISTIC,
                "abilities": [
                    {"name": "normalize_fields", "server": MCPServer.COMMON},
                    {"name": "enrich_records", "server": MCPServer.ATLAS},
                    {"name": "add_flags_calculations", "server": MCPServer.COMMON}
                ],
                "description": "🛠️ Prepare and enrich data"
            },
            "ASK": {
                "mode": StageMode.HUMAN_INTERACTION,
                "abilities": [
                    {"name": "clarify_question", "server": MCPServer.ATLAS}
                ],
                "description": "❓ Ask clarifying questions"
            },
            "WAIT": {
                "mode": StageMode.DETERMINISTIC,
                "abilities": [
                    {"name": "extract_answer", "server": MCPServer.ATLAS}
                ],
                "description": "⏳ Wait for customer response"
            },
            "RETRIEVE": {
                "mode": StageMode.DETERMINISTIC,
                "abilities": [
                    {"name": "knowledge_base_search", "server": MCPServer.ATLAS}
                ],
                "description": "📚 Search knowledge base"
            },
            "DECIDE": {
                "mode": StageMode.NON_DETERMINISTIC,
                "abilities": [
                    {"name": "solution_evaluation", "server": MCPServer.COMMON},
                    {"name": "escalation_decision", "server": MCPServer.ATLAS}
                ],
                "description": "⚖️ Make decisions"
            },
            "UPDATE": {
                "mode": StageMode.DETERMINISTIC,
                "abilities": [
                    {"name": "update_ticket", "server": MCPServer.ATLAS},
                    {"name": "close_ticket", "server": MCPServer.ATLAS}
                ],
                "description": "🔄 Update ticket status"
            },
            "CREATE": {
                "mode": StageMode.DETERMINISTIC,
                "abilities": [
                    {"name": "response_generation", "server": MCPServer.COMMON}
                ],
                "description": "✍️ Generate customer response"
            },
            "DO": {
                "mode": StageMode.DETERMINISTIC,
                "abilities": [
                    {"name": "execute_api_calls", "server": MCPServer.ATLAS},
                    {"name": "trigger_notifications", "server": MCPServer.ATLAS}
                ],
                "description": "🏃 Execute actions"
            },
            "COMPLETE": {
                "mode": StageMode.DETERMINISTIC,
                "abilities": [],  # Just output final payload
                "description": "✅ Complete workflow"
            }
        }
    
    async def execute_stage(self, stage_name: str, payload: CustomerSupportPayload) -> CustomerSupportPayload:
        """Execute a single stage of the workflow"""
        stage_config = self.stage_config[stage_name]
        
        logger.info(f"\n{'='*60}")
        logger.info(f"{stage_config['description']} - {stage_name}")
        logger.info(f"Mode: {stage_config['mode'].value}")
        logger.info(f"{'='*60}")
        
        # Execute based on stage mode
        if stage_config["mode"] == StageMode.DETERMINISTIC:
            payload = await self._execute_deterministic_stage(stage_name, stage_config, payload)
        elif stage_config["mode"] == StageMode.NON_DETERMINISTIC:
            payload = await self._execute_non_deterministic_stage(stage_name, stage_config, payload)
        elif stage_config["mode"] == StageMode.HUMAN_INTERACTION:
            payload = await self._execute_human_interaction_stage(stage_name, stage_config, payload)
        
        # Track stage completion
        payload.stage_history.append(f"{stage_name}_{datetime.now().strftime('%H:%M:%S')}")
        logger.info(f"✅ {stage_name} completed")
        
        return payload
    
    async def _execute_deterministic_stage(self, stage_name: str, config: Dict, payload: CustomerSupportPayload) -> CustomerSupportPayload:
        """Execute abilities in sequence (deterministic)"""
        if not config["abilities"]:
            if stage_name == "INTAKE":
                logger.info(f"📋 Accepted payload for ticket: {payload.ticket_id}")
            elif stage_name == "COMPLETE":
                logger.info("🎯 Final payload ready for output")
            return payload
        
        for ability in config["abilities"]:
            ability_name = ability["name"]
            server = ability["server"]
            
            # Route to correct MCP server
            if server == MCPServer.COMMON:
                result = await self.common_client.execute_ability(ability_name, payload)
            else:  # MCPServer.ATLAS
                result = await self.atlas_client.execute_ability(ability_name, payload)
            
            # Update payload with results
            self._update_payload_with_result(ability_name, result, payload)
            
        return payload
    
    async def _execute_non_deterministic_stage(self, stage_name: str, config: Dict, payload: CustomerSupportPayload) -> CustomerSupportPayload:
        """Execute with dynamic decision making (non-deterministic)"""
        logger.info("🎯 Using dynamic orchestration logic")
        
        # First, evaluate solutions
        solution_result = await self.common_client.execute_ability("solution_evaluation", payload)
        payload.solution_scores = solution_result.get("scores", [])
        
        # Make escalation decision based on scores
        if payload.solution_scores:
            best_score = max(s["score"] for s in payload.solution_scores)
            best_solution = max(payload.solution_scores, key=lambda x: x["score"])
            
            logger.info(f"🏆 Best solution: {best_solution['solution']} (score: {best_score})")
            
            if best_score < 90:
                logger.info(f"🚨 ESCALATING: Score {best_score} < 90 threshold")
                escalation_result = await self.atlas_client.execute_ability("escalation_decision", payload)
                payload.escalation_decision = True
            else:
                logger.info(f"✅ AI RESOLVING: Score {best_score} >= 90 threshold")
                payload.escalation_decision = False
        
        return payload
    
    async def _execute_human_interaction_stage(self, stage_name: str, config: Dict, payload: CustomerSupportPayload) -> CustomerSupportPayload:
        """Handle human interaction stages"""
        logger.info("👥 Human interaction stage")
        
        # Generate clarification question
        clarify_result = await self.atlas_client.execute_ability("clarify_question", payload)
        payload.clarification_needed = True
        
        # In a real system, we'd wait for human input
        # For demo, we simulate having received an answer
        logger.info(f"❓ Would ask: {clarify_result.get('question', 'Can you provide more details?')}")
        logger.info("⏳ (In real system, would wait for customer response)")
        
        return payload
    
    def _update_payload_with_result(self, ability_name: str, result: Dict, payload: CustomerSupportPayload):
        """Update payload with ability execution results"""
        if ability_name == "parse_request_text":
            payload.parsed_data = result
        elif ability_name == "extract_entities":
            payload.extracted_entities = result
        elif ability_name == "normalize_fields":
            payload.normalized_fields = result
        elif ability_name == "enrich_records":
            payload.enriched_records = result
        elif ability_name == "add_flags_calculations":
            payload.flags_calculations = result
        elif ability_name == "extract_answer":
            payload.clarification_answer = result.get("answer")
        elif ability_name == "knowledge_base_search":
            payload.knowledge_base_results = result.get("articles", [])
        elif ability_name == "update_ticket" or ability_name == "close_ticket":
            if payload.ticket_updates is None:
                payload.ticket_updates = {}
            payload.ticket_updates.update(result)
        elif ability_name == "response_generation":
            payload.generated_response = result.get("response")
        elif ability_name == "execute_api_calls":
            payload.api_results = result
        elif ability_name == "trigger_notifications":
            payload.notifications_sent = [k for k, v in result.items() if v is True]
    
    async def run_complete_workflow(self, input_data: Dict) -> CustomerSupportPayload:
        """Run the complete 11-stage customer support workflow"""
        logger.info("🚀 STARTING COMPLETE LANGGRAPH CUSTOMER SUPPORT WORKFLOW")
        logger.info(f"📅 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Initialize payload
        payload = CustomerSupportPayload(**input_data)
        logger.info(f"🎫 Processing ticket: {payload.ticket_id}")
        
        # Define the complete stage execution order
        stages = [
            "INTAKE",     # 📥 Accept payload
            "UNDERSTAND", # 🧠 Parse + extract entities  
            "PREPARE",    # 🛠️ Normalize + enrich + calculate
            "ASK",        # ❓ Clarify if needed
            "WAIT",       # ⏳ Extract customer answer
            "RETRIEVE",   # 📚 Search knowledge base
            "DECIDE",     # ⚖️ Evaluate solutions (non-deterministic!)
            "UPDATE",     # 🔄 Update + close ticket
            "CREATE",     # ✍️ Generate response
            "DO",         # 🏃 Execute APIs + notifications
            "COMPLETE"    # ✅ Output final payload
        ]
        
        # Execute each stage in order
        for i, stage in enumerate(stages, 1):
            logger.info(f"\n🎯 STAGE {i}/11: {stage}")
            payload = await self.execute_stage(stage, payload)
        
        # Final summary
        logger.info(f"\n{'='*60}")
        logger.info("🎉 WORKFLOW COMPLETED SUCCESSFULLY!")
        logger.info(f"📊 Total stages executed: {len(payload.stage_history)}")
        logger.info(f"🚨 Escalated to human: {payload.escalation_decision}")
        logger.info(f"💬 Response generated: {'Yes' if payload.generated_response else 'No'}")
        logger.info(f"📧 Notifications sent: {len(payload.notifications_sent or [])}")
        logger.info(f"{'='*60}")
        
        return payload

# ═══════════════════════════════════════════════════════════════════════════════
# DEMO EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

async def main():
    """Complete demo of the 11-stage LangGraph agent"""
    
    # Initialize agent
    agent = LangGraphCustomerSupportAgent()
    
    # Test scenarios
    test_cases = [
        {
            "name": "🔥 High Priority Billing Issue",
            "data": {
                "customer_name": "Sarah Wilson",
                "email": "sarah.wilson@email.com",
                "query": "I was charged three times for the same subscription! This is urgent!",
                "priority": "HIGH",
                "ticket_id": "TKT-2024-001"
            }
        },
        {
            "name": "🔧 Technical Issue",
            "data": {
                "customer_name": "Mike Chen",
                "email": "mike.chen@techcorp.com",
                "query": "The mobile app keeps crashing when I try to upload documents",
                "priority": "MEDIUM", 
                "ticket_id": "TKT-2024-002"
            }
        }
    ]
    
    # Run each test case
    for i, test_case in enumerate(test_cases, 1):
        logger.info(f"\n{'█'*80}")
        logger.info(f"🧪 TEST CASE {i}: {test_case['name']}")
        logger.info(f"{'█'*80}")
        
        logger.info("📋 INPUT DATA:")
        for key, value in test_case["data"].items():
            logger.info(f"   {key}: {value}")
        
        # Run the complete workflow
        start_time = datetime.now()
        final_payload = await agent.run_complete_workflow(test_case["data"])
        end_time = datetime.now()
        
        execution_time = (end_time - start_time).total_seconds()
        
        # Results summary
        logger.info(f"\n📊 EXECUTION SUMMARY:")
        logger.info(f"   ⏱️  Total time: {execution_time:.2f} seconds")
        logger.info(f"   🔄 Stages: {' → '.join([s.split('_')[0] for s in final_payload.stage_history])}")
        logger.info(f"   🚨 Escalated: {final_payload.escalation_decision}")
        logger.info(f"   📝 Final response: {final_payload.generated_response[:100] if final_payload.generated_response else 'None'}...")
        
        # Save detailed results
        results_file = f"test_results_{test_case['data']['ticket_id']}.json"
        with open(results_file, "w") as f:
            json.dump(asdict(final_payload), f, indent=2, default=str)
        logger.info(f"   💾 Detailed results saved to: {results_file}")
        
        if i < len(test_cases):
            logger.info("\n⏸️  Waiting 2 seconds before next test...\n")
            await asyncio.sleep(2)
    
    logger.info(f"\n🎊 ALL TESTS COMPLETED!")
    logger.info("📁 Check the JSON files for detailed execution logs")

if __name__ == "__main__":
    asyncio.run(main())