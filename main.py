import asyncio
from langchain_core.messages import HumanMessage, AIMessage
from assistant_graph import agent_graph
from voice_utils import record_audio_until_stop, play_audio

async def main():
    print("--- Telugu Voice Agent Started ---")
    config = {"configurable": {"thread_id": "demo-1"}}
    
    while True:
        try:
            # 1. Listen
            user_text = await record_audio_until_stop()
            
            if "exit" in user_text.lower():
                break
            if not user_text.strip():
                continue

            # 2. Think (Stream)
            print("🤔 Thinking...")
            input_msg = HumanMessage(content=user_text)
            async for event in agent_graph.astream_events({"messages": [input_msg]}, config=config, version="v1"):
                pass # Just consume the stream to let it finish

            # 3. Speak
            state = agent_graph.get_state(config)
            last_msg = state.values["messages"][-1]
            
            if isinstance(last_msg, AIMessage):
                await play_audio(last_msg.content)

        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    asyncio.run(main())