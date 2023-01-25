from islamweb import IslamWeb

start = time.perf_counter()
islamWeb = IslamWeb(8000)
# asyncio.run(islamWeb.save_articles_link())
# asyncio.run(islamWeb.save_entities('articles','file_name_here'))
# asyncio.run(islamWeb.get_question_links())
# asyncio.run(islamWeb.save_entities('questions','file_name_here'))
# asyncio.run(islamWeb.save_consult_link())
# asyncio.run(islamWeb.save_entities('consults','file_name_here'))
stop = time.perf_counter()
print("time taken:", stop - start)
