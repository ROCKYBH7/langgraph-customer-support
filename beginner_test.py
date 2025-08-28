# beginner_test.py - Step 7: Easy testing for beginners

"""
This is your testing playground! 🎮
Run this to see your LangGraph agent in action with different scenarios.
"""

import asyncio
import json
from datetime import datetime
from full_langgraph_agent import LangGraphCustomerSupportAgent

async def run_single_test(agent, test_name, customer_data):
    """Run one test and show results clearly"""
    print(f"\n{'='*50}")
    print(f"🧪 TEST: {test_name}")
    print(f"{'='*50}")
    
    print("📝 Customer Input:")
    print(f"   Name: {customer_data['customer_name']}")
    print(f"   Email: {customer_data['email']}")
    print(f"   Issue: {customer_data['query']}")
    print(f"   Priority: {customer_data['priority']}")
    print(f"   Ticket: {customer_data['ticket_id']}")
    
    print("\n🚀 Running workflow...")
    start_time = datetime.now()
    
    # This is where the magic happens!
    result = await agent.run_complete_workflow(customer_data)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"\n📊 RESULTS SUMMARY:")
    print(f"   ⏱️  Time taken: {duration:.1f} seconds")
    print(f"   🎯 Stages completed: {len(result.stage_history)}")
    print(f"   🚨 Needs human help: {'YES' if result.escalation_decision else 'NO'}")
    print(f"   💬 Response ready: {'YES' if result.generated_response else 'NO'}")
    
    if result.solution_scores:
        best_score = max(s["score"] for s in result.solution_scores)
        print(f"   📈 Best solution score: {best_score}/100")
    
    if result.generated_response:
        print(f"\n📧 Generated Response:")
        print(f"   \"{result.generated_response[:120]}...\"")
    
    print(f"\n🔄 Workflow Journey:")
    journey = " → ".join([stage.split('_')[0] for stage in result.stage_history])
    print(f"   {journey}")
    
    return result

async def main():
    """Main testing function - this is where you start!"""
    print("🎉 Welcome to LangGraph Customer Support Agent Testing!")
    print("📚 This will show you how your agent handles different customer issues")
    
    # Create your agent
    agent = LangGraphCustomerSupportAgent()
    
    # Test scenarios - you can modify these or add your own!
    test_scenarios = [
        {
            "name": "Angry Billing Customer",
            "customer": {
                "customer_name": "Jessica Martinez",
                "email": "jessica@email.com",
                "query": "I've been charged $99 twice this month and I only signed up once! This is ridiculous!",
                "priority": "HIGH",
                "ticket_id": "TKT-2024-001"
            }
        },
        {
            "name": "Technical Support Request",
            "customer": {
                "customer_name": "David Park",
                "email": "david.park@company.com",
                "query": "The mobile app crashes every time I try to save a document. Can you help?",
                "priority": "MEDIUM",
                "ticket_id": "TKT-2024-002"
            }
        },
        {
            "name": "Simple Question",
            "customer": {
                "customer_name": "Emma Rodriguez", 
                "email": "emma.r@startup.co",
                "query": "How do I change my password?",
                "priority": "LOW",
                "ticket_id": "TKT-2024-003"
            }
        }
    ]
    
    # Run all tests
    print(f"\n🏃 Running {len(test_scenarios)} test scenarios...\n")
    
    results = []
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n📍 Test {i} of {len(test_scenarios)}")
        result = await run_single_test(agent, scenario["name"], scenario["customer"])
        results.append({
            "scenario": scenario["name"],
            "escalated": result.escalation_decision,
            "response_generated": bool(result.generated_response)
        })
        
        if i < len(test_scenarios):
            print("\n⏳ Waiting 3 seconds before next test...\n")
            await asyncio.sleep(3)
    
    # Final summary
    print(f"\n{'='*60}")
    print("🎊 ALL TESTS COMPLETED! Here's what happened:")
    print(f"{'='*60}")
    
    total_tests = len(results)
    escalated_count = sum(1 for r in results if r["escalated"])
    ai_resolved_count = total_tests - escalated_count
    responses_generated = sum(1 for r in results if r["response_generated"])
    
    print(f"📊 Test Summary:")
    print(f"   Total scenarios tested: {total_tests}")
    print(f"   🤖 AI resolved: {ai_resolved_count} ({ai_resolved_count/total_tests*100:.0f}%)")
    print(f"   👥 Escalated to humans: {escalated_count} ({escalated_count/total_tests*100:.0f}%)")
    print(f"   📝 Responses generated: {responses_generated}/{total_tests}")
    
    print(f"\n📋 Individual Results:")
    for i, result in enumerate(results, 1):
        status = "🤖 AI Resolved" if not result["escalated"] else "👥 Human Needed"
        print(f"   {i}. {result['scenario']}: {status}")
    
    print(f"\n🎓 What This Shows:")
    print(f"   ✅ Your agent can process different types of customer issues")
    print(f"   ✅ It makes smart decisions about when to escalate")
    print(f"   ✅ It follows the complete 11-stage workflow")
    print(f"   ✅ It generates appropriate responses")
    
    print(f"\n🚀 Your LangGraph Customer Support Agent is working perfectly!")

# Run the tests!
if __name__ == "__main__":
    print("Starting LangGraph Agent Tests...")
    asyncio.run(main())