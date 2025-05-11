import pytest
from books_collector import BooksCollector


class TestBooksCollector:

    @pytest.fixture
    def collector(self):
        return BooksCollector()

    def test_add_valid_book(self, collector):
        collector.add_new_book("Война и мир")
        assert "Война и мир" in collector.books_genre
        assert collector.books_genre["Война и мир"] == ""

    def test_add_duplicate_book(self, collector):
        collector.add_new_book("1984")
        collector.add_new_book("1984")
        assert len(collector.books_genre) == 1

    @pytest.mark.parametrize("name, expected", [
        ("A" * 40, True),
        ("A" * 41, False),
        ("", False)
    ])
    def test_add_books_with_different_lengths(self, collector, name, expected):
        collector.add_new_book(name)
        assert (name in collector.books_genre) == expected

    def test_set_valid_genre(self, collector):
        collector.add_new_book("Ночной дозор")
        collector.set_book_genre("Ночной дозор", "Фантастика")
        assert collector.get_book_genre("Ночной дозор") == "Фантастика"

    def test_set_invalid_genre(self, collector):
        collector.add_new_book("Собачье сердце")
        collector.set_book_genre("Собачье сердце", "История")
        assert collector.get_book_genre("Собачье сердце") == ""

    def test_get_nonexistent_book_genre(self, collector):
        assert collector.get_book_genre("Несуществующая книга") is None

    def test_get_books_by_genre(self, collector):
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.set_book_genre("Книга1", "Детективы")
        collector.set_book_genre("Книга2", "Детективы")
        result = collector.get_books_with_specific_genre("Детективы")
        assert len(result) == 2
        assert "Книга1" in result
        assert "Книга2" in result

    def test_get_children_books(self, collector):
        collector.add_new_book("Ну погоди!")
        collector.add_new_book("Оно")
        collector.set_book_genre("Ну погоди!", "Мультфильмы")
        collector.set_book_genre("Оно", "Ужасы")
        result = collector.get_books_for_children()
        assert "Ну погоди!" in result
        assert "Оно" not in result

    def test_add_to_favorites(self, collector):
        collector.add_new_book("Мастер и Маргарита")
        collector.add_book_in_favorites("Мастер и Маргарита")
        assert "Мастер и Маргарита" in collector.get_list_of_favorites_books()

    def test_add_to_favorites_twice(self, collector):
        collector.add_new_book("Преступление и наказание")
        collector.add_book_in_favorites("Преступление и наказание")
        collector.add_book_in_favorites("Преступление и наказание")
        assert len(collector.get_list_of_favorites_books()) == 1

    def test_remove_from_favorites(self, collector):
        collector.add_new_book("Анна Каренина")
        collector.add_book_in_favorites("Анна Каренина")
        collector.delete_book_from_favorites("Анна Каренина")
        assert "Анна Каренина" not in collector.get_list_of_favorites_books()

    def test_remove_nonexistent_from_favorites(self, collector):
        collector.delete_book_from_favorites("Несуществующая книга")
        assert len(collector.get_list_of_favorites_books()) == 0

    def test_initial_state(self, collector):
        assert collector.books_genre == {}
        assert collector.favorites == []
        assert len(collector.genre) == 5
        assert len(collector.genre_age_rating) == 2

    def test_get_all_books(self, collector):
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        assert len(collector.get_books_genre()) == 2