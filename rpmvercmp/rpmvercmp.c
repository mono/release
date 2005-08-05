/*
 * simple program to return sorted strings using rpmvercmp
 *
 * Compile with: gcc rpmvercmp.c -lrpm -lrpmio -lrpmdb -lpopt -o rpmvercmp
 *
 * Wade Berrier <wberrier@novell.com>
 *
 */

#include <rpm/rpmlib.h>

void sort(char **text, int *index_map, int size)
{
	int swap_made = 1;
	int i;
	int temp_index;

	while(swap_made) {

		swap_made = 0;

		for(i = 0; i < size - 1; i++) {
			
			/* If the first is of higher precedence than the second */	
			if(rpmvercmp(text[index_map[i]], text[index_map[i + 1]]) == 1) {
			
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
	/*printf("\n");*/
}


int main(int argc, char *argv[])
{
	int return_val;
	int i = 0;

	int index_map[argc];

	if(argc < 2) {
		/* printf("Usage: rpmvercmp string1 string2 ... string[n]\n"); */
		exit(1);

	}

	/* Init map */
	for(i = 0; i < argc; i++)
		index_map[i] = i;

	sort(&argv[1], index_map, argc - 1);
	print_list(&argv[1], index_map, argc - 1);

}
