from infrastructure.rag.rag_factory import create_rag_service


def main():
    rag = create_rag_service()

    queries = [
        "سردرد شدید دارم",
        "I have severe headache",
        "درد قفسه سینه دارم",
        "تب و لرز دارم",
        "درد شدید شکم دارم",
        "من ماشینم را دوست دارم",
    ]

    print("=" * 70)
    print("EMBEDDING / VECTOR DISTANCE EVALUATION")
    print("=" * 70)

    for query in queries:
        results = rag.retrieve(
            query=query,
            top_k=1,
        )

        print(f"\nQuery: {query}")

        if not results:
            print("No result")
            continue

        result = results[0]

        print(
            f"Source: {result['source']}"
        )

        print(
            f"Distance: {result['distance']:.4f}"
        )


if __name__ == "__main__":
    main()