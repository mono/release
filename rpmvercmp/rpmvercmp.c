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
gint version_compare(const gchar *string1, const gchar *string2)
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

void print_num(gchar *string, gpointer *user_data)
{
	printf("%s\n", string);
}

gint main(int argc, char *argv[])
{
	gint i = 1;

	GList *list = NULL;

	if(argc < 2) {
		/* Return 0 here signifying an empty list */
		exit(0);
	}

	/* Load list */
	for(i = 1; i < argc; i++) {
		list = g_list_append(list, argv[i]);
	}

	list = g_list_sort(list, (GCompareFunc)version_compare);
	g_list_foreach(list, (GFunc)print_num, NULL);

	g_list_free(list);

	exit(0);

}


