import time
import curses

def visualize(window, write_center, x_margin, book, correct, wrong, errors, start_time, debug_string=None):

    sentence = book.current_line()
    preceeding = book.get_preceeding_lines(2)
    following = book.get_following_lines(10)

    window.clear()

    if debug_string is not None:
        window.addstr(write_center - 8, x_margin, debug_string)

    status_sentence = get_status_string(start_time, correct, errors, book)

    window.addstr(write_center - 4, x_margin, "statusstr", curses.color_pair(curses.COLOR_GREEN))

    for pre_i in range(len(preceeding)):
        line = preceeding[pre_i]
        window.addstr(write_center + 3 - len(preceeding) + pre_i, x_margin, line, curses.color_pair(curses.COLOR_BLUE))

    for i in range(len(following)):
        line = following[i]
        window.addstr(write_center + 4 + i, x_margin, line, curses.color_pair(curses.COLOR_BLUE))

    window.addstr(write_center - 2, x_margin, status_sentence)
    write_colored_sentence(window, x_margin, write_center + 3, sentence, correct, wrong)

    window.refresh()



def write_colored_sentence(window, x, y, target_sent, correct, wrong):

    corr_str = target_sent[:correct]
    wrong_str = target_sent[correct:correct+wrong]
    rest = target_sent[correct+wrong:]

    window.addstr(y, x, corr_str, curses.color_pair(curses.COLOR_GREEN))
    window.addstr(y, x + len(corr_str), wrong_str, curses.color_pair(curses.COLOR_RED))
    window.addstr(y, x + len(corr_str) + len(wrong_str), rest)
    window.move(y, x + len(corr_str) + len(wrong_str))


def get_status_string(start_time, correct, wrong, book):

    elapsed_time = time.time() - start_time

    wpm = book.get_wpm(elapsed_time)

    return '{} seconds, {} correct, {} errors, {:.1f} wpm'.format(int(elapsed_time), correct, wrong, wpm)