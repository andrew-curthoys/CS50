#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[1];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    unsigned char *block = (unsigned char *) malloc(512 * sizeof(char));
    char *filename = (char *) malloc(7 * sizeof(char));
    FILE *img;

    int n = 0;
    int file_num = 0;

    while (fread(block, 512 * sizeof(char), 1, inptr) > 0)
    {
        // check if the block is the beginning of a new JPEG file
        if
        (
            block[0] == 0xff &&
            block[1] == 0xd8 &&
            block[2] == 0xff &&
            (block[3] & 0xf0) == 0xe0
        )
        {
            // check if this is the first JPEG on the card & create a new file to store the JPEG
            if (file_num == 0)
            {
                // create file to store JPEG
                sprintf(filename, "%03i.jpg", file_num);
                img = fopen(filename, "w");

                // increment file_num
                file_num++;
            }
            else
            {
                fclose(img);

                // create file to store JPEG
                sprintf(filename, "%03i.jpg", file_num);
                img = fopen(filename, "w");

                // increment file_num
                file_num++;
            }

            // write contents of buffer to file
            fwrite(block, 512 * sizeof(char), 1, img);
        }
        else
        {
            if (file_num > 0)
            {
                // write contents of buffer to file
                fwrite(block, 512 * sizeof(char), 1, img);
            }
        }
    }

    free(block);
    free(filename);

}
