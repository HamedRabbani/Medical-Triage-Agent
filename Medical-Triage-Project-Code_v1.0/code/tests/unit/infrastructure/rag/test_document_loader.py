from infrastructure.rag.document_loader import DocumentLoader


def test_document_loader_loads_txt_files(tmp_path):

    file = tmp_path / "headache.txt"

    file.write_text(
        "Headache may be caused by several conditions.",
        encoding="utf-8",
    )

    loader = DocumentLoader(
        knowledge_directory=str(tmp_path)
    )

    documents = loader.load()

    assert len(documents) == 1

    assert (
        documents[0]["content"]
        == "Headache may be caused by several conditions."
    )

    assert documents[0]["source"].endswith(
        "headache.txt"
    )