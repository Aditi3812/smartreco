from app.services.mesh_llm_service import (
    mesh_llm_service
)


result = mesh_llm_service.generate(

    system_prompt="""
    You are SmartReco,
    an AI recommendation assistant.
    Recommend learning courses.
    """,

    user_prompt="""
    User likes AI and Python.
    Suggest one course.
    """
)


print("\n")
print("="*60)
print("MESH RESPONSE")
print("="*60)

print(result)

print("="*60)