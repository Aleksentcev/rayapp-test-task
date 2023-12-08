import asyncio


async def process_text_async(text):
    await asyncio.sleep(1)
    processed_text = text.upper()
    return processed_text

# Я знаю, что это крайне странное применение,
# но больше ничего стоящего не придумал.
