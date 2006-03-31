/*
 *
 * simple program to return sorted strings using rpmvercmp
 *
 * Wade Berrier <wberrier@novell.com>
 *
 * TODO: Problem, "1.1.10.1" and "1.1.10-1" are considered equivalent according to rpmvercmp (solved)
 *
 */

#include <rpm/rpmlib.h>
#include <glib-2.0/glib.h>

/* Uses rpmvercmp but fixes it's brokenness */
int version_compare(const char *string1, const char *string2)
{
	gchar **string1_list;
	gchar **string2_list;

	int difference_found = 0;
	int result = 0;
	int i = 0;

	string1_list = g_strsplit (string1, "-", 0);
	string2_list = g_strsplit (string2, "-", 0);

	while(!difference_found) { 

		if(string1_list[i] == NULL && string2_list[i] == NULL) { 
			/* We're at the end, and we've still found no differences, end it */
			result = 0;
			difference_found = 1;
		} else if(string1_list[i] != NULL && string2_list[i] == NULL) {
			/* The first string has something while next is empty, it wins */
			result = 1;
			difference_found = 1;
		} else if(string1_list[i] == NULL && string2_list[i] != NULL) {
			/* The first string is empty, second (containing something) wins */
			result = -1;
			difference_found = 1;
		} else {
			/* Both strings are not NULL */

			result = rpmvercmp(string1_list[i], string2_list[i]);

			if (result > 0 ) { 
				/* Greater than */
				difference_found = 1;

			} else if( result < 0 ) { 
				/* Less than */
				difference_found = 1;
			} else {
				/* Equal to, continue to next round */
			}
		}

		i++;

	}

	g_strfreev(string1_list);
	g_strfreev(string2_list);

	return (result);

}


/* Simple bubble sort */
/* Args: array of strings, map to signify order, size, and function pointer to use for comparison */
void sort(char **text, int *index_map, int size, int (compare_func)(const char *, const char*))
{
	int swap_made = 1;
	int i;
	int temp_index;

	while(swap_made) {

		swap_made = 0;

		for(i = 0; i < size - 1; i++) {
			
			/* If the first is of higher precedence than the second */	
			if(compare_func(text[index_map[i]], text[index_map[i + 1]]) == 1) {
			
				temp_index = index_map[i];
				index_map[i] = index_map[i + 1];
				index_map[i + 1] = temp_index;

				swap_made = 1;
			}

		}
	}
}

void print_list(char **text, int *index_map, int size)
{
	int i = 0;
	for(i = 0; i < size; i++)
		printf("%s\n", text[index_map[i]]);
}


int main(int argc, char *argv[])
{
	int return_val;
	int i = 0;

	int index_map[argc];

	if(argc < 2) {
		/* Return 0 here signifying an empty list */
		exit(0);
	}

	/* Init map */
	for(i = 0; i < argc; i++)
		index_map[i] = i;

	sort(&argv[1], index_map, argc - 1, &version_compare);

	print_list(&argv[1], index_map, argc - 1);

	exit(0);

}

