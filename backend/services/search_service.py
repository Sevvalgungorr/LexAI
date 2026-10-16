
def search_decisions_service(query: str, top_k: int) -> dict:
    """
    Hukuki karar arama işlemlerini yönetir.
    Şimdilik örnek yanıt oluşturur.
    """

    return {
        "query": query,
        "top_k": top_k,
        "message": "Arama isteği başarıyla alındı."
    }
