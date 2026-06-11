from primerpro import GraphemeTaughtOrder, Syllable, Word

from .fixtures import create_bantu_like_settings, taught


def test_word_is_buildable_when_every_syllable_grapheme_is_taught_exactly():
    """A word is buildable when each syllable grapheme is taught."""
    settings = create_bantu_like_settings()
    word = Word("mbata", settings)

    assert word.is_buildable_word(taught("mb", "a", "t"))


def test_word_is_not_buildable_when_any_grapheme_is_untaught():
    """A word is not buildable when any grapheme is untaught."""
    settings = create_bantu_like_settings()
    word = Word("mbata", settings)

    assert not word.is_buildable_word(taught("m", "b", "a", "t"))


def test_initial_underscore_convention_allows_syllable_initial_graphemes_only():
    """Initial marker t_ only matches syllable-initial positions."""
    settings = create_bantu_like_settings()
    initial = Word("ta", settings)
    medial = Syllable("ata", settings)
    graphemes = taught("t_", "a")

    assert initial.is_buildable_word(graphemes)
    assert not medial.is_buildable(graphemes)


def test_final_underscore_convention_allows_syllable_final_graphemes_only():
    """Final marker _t only matches syllable-final positions."""
    settings = create_bantu_like_settings()
    final = Word("at", settings)
    initial = Word("ta", settings)
    graphemes = taught("_t", "a")

    assert final.is_buildable_word(graphemes)
    assert not initial.is_buildable_word(graphemes)


def test_position_markers_are_evaluated_per_syllable_not_only_per_word():
    """Test that position markers are evaluated per syllable, not just per word."""
    settings = create_bantu_like_settings()
    word = Word("ta.na", settings)

    assert word.is_buildable_word(taught("t_", "n_", "a"))


def test_grapheme_taught_order_missing_check_strips_positional_underscores():
    """Missing-grapheme checks strip positional underscores."""
    settings = create_bantu_like_settings()
    graphemes_taught = GraphemeTaughtOrder(settings)
    graphemes_taught.add_grapheme("t_")
    graphemes_taught.add_grapheme("_n")
    graphemes_taught.add_grapheme("zz")

    missing = graphemes_taught.get_missing_graphemes()

    assert "t_" not in missing
    assert "_n" not in missing
    assert "zz" in missing
