import treetaggerwrapper 
import sys

#######################################################################

def indexes_lists_of_needles_inside_haystack(haystack, needle):  # obviously needs a better name ...
    if not needle:
        return
    # just optimization
    lengthneedle = len(needle)
    firstneedle = needle[0]
    for idx, item in enumerate(haystack):
        if item == firstneedle:
            if haystack[idx:idx+lengthneedle] == needle:
                yield tuple(range(idx, idx+lengthneedle))

def get_title_part_matching_target_sequence(title_tags_list, pos_target_sequences):

    title_pos_list = [tag.pos for tag in title_tags_list if hasattr(tag, 'pos')]

    for pos_list_to_look_for in pos_target_sequences:

        indexes_lists_of_target_inside_title = list(indexes_lists_of_needles_inside_haystack(title_pos_list ,pos_list_to_look_for))

        if len(indexes_lists_of_target_inside_title) > 0:
            indexes_list_of_target_inside_title = indexes_lists_of_target_inside_title[0]

            words_list_to_return = [title_tags_list[index].word for index in indexes_list_of_target_inside_title]

            return ' '.join(words_list_to_return)

#######################################################################        

report_title_list = ' '.join(sys.argv[1:]).split(',')

with open('./sorted_target_pos_sequences.txt') as sorted_target_pos_sequences_file:
    sorted_pos_sequences = [pos_sequence.split(',') for pos_sequence in sorted_target_pos_sequences_file.read().splitlines()]

tagger = treetaggerwrapper.TreeTagger(TAGLANG="it", TAGDIR="./treetagger")

tagged_titles = [
    treetaggerwrapper.make_tags(tagger.tag_text(report_title)) for report_title in report_title_list
    ]    

refined_titles = [
    get_title_part_matching_target_sequence(tagged_title, sorted_pos_sequences) for tagged_title in tagged_titles
    ]

refined_titles = ['' if refined_titles is None else refined_titles for refined_titles in refined_titles]

for i in range(len(refined_titles)):
    print(refined_titles[i])
