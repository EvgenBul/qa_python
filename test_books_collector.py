import pytest
from books_collector import BooksCollector


class TestBooksCollector:

    @pytest.fixture
    def collector(self):
        return BooksCollector()

    def test_add_new_book_valid_name(self, collector):
        collector.add_new_book("Ночной дозор")
        assert "Ночной дозор" in collector.books_genre
        assert collector.books_genre["Ночной дозор"] == ""

    @pytest.mark.parametrize("name,expected", [
        ("", False),
        ("x" * 41, False),
        ("Ночной дозор", True)
    ])
    def test_add_new_book_invalid_name(self, collector, name, expected):
        collector.add_new_book("Ночной дозор")
        initial_count = len(collector.books_genre)
        collector.add_new_book(name)
        if expected:
            assert len(collector.books_genre) == initial_count
        else:
            assert len(collector.books_genre) == initial_count

    def test_set_book_genre_valid(self, collector):
        collector.add_new_book("Ночной дозор")
        collector.set_book_genre("Ночной дозор", "Фантастика")
        assert collector.get_book_genre("Ночной дозор") == "Фантастика"

    def test_set_book_genre_invalid(self, collector):
        collector.add_new_book("Ночной дозор")
        collector.set_book_genre("Ночной дозор", "Несуществующий жанр")
        assert collector.get_book_genre("Ночной дозор") == ""

    def test_get_books_with_specific_genre(self, collector):
        collector.add_new_book("Книга 1")
        collector.add_new_book("Книга 2")
        collector.set_book_genre("Книга 1", "Фантастика")
        collector.set_book_genre("Книга 2", "Фантастика")
        result = collector.get_books_with_specific_genre("Фантастика")
        assert len(result) == 2
        assert "Книга 1" in result
        assert "Книга 2" in result

    def test_get_books_for_children(self, collector):
        collector.add_new_book("Мультик")
        collector.add_new_book("Ужастик")
        collector.set_book_genre("Мультик", "Мультфильмы")
        collector.set_book_genre("Ужастик", "Ужасы")
        children_books = collector.get_books_for_children()
        assert "Мультик" in children_books
        assert "Ужастик" not in children_books

    def test_add_and_remove_favorites(self, collector):
        collector.add_new_book("Гарри Поттер")
        collector.add_book_in_favorites("Гарри Поттер")
        assert "Гарри Поттер" in collector.get_list_of_favorites_books()
        collector.delete_book_from_favorites("Гарри Поттер")
        assert "Гарри Поттер" not in collector.get_list_of_favorites_books()

    def test_add_to_favorites_twice(self, collector):
        collector.add_new_book("Гарри Поттер")
        collector.add_book_in_favorites("Гарри Поттер")
        collector.add_book_in_favorites("Гарри Поттер")
        assert len(collector.get_list_of_favorites_books()) == 1

    @pytest.mark.parametrize("name,genre,expected", [
        ("Книга 1", "Фантастика", True),
        ("Книга 2", "Несуществующий жанр", False),
        ("Несуществующая книга", "Фантастика", False)
    ])

    def test_set_and_get_genre_parametrized(self, collector, name, genre, expected):
        collector.add_new_book("Книга 1")
        collector.set_book_genre(name, genre)
        assert (collector.get_book_genre(name) == genre) == expected