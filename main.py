from textgenrnn import textgenrnn
from scrape_wp import write_file_from_wordpress

if __name__ == '__main__':
    # configurable
    site_first_page = 'https://tiraas.net/2014/08/20/book-1-prologue/'
    work_filename = 'tgab.txt'
    output_filename = 'output.txt'
    # operant code
    write_file_from_wordpress(site_first_page, work_filename)  # this line can be removed if not first run
    ai = textgenrnn()
    ai.train_from_largetext_file(work_filename)
    ai.generate_to_file(output_filename, 100)

