#include <unistd.h>
#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>
// will use magic numbers from:
// https://en.wikipedia.org/wiki/Magic_number_(programming)
#define SUPERMAGIC_HEAD 0xcafebabe
#define SUPERMAGIC_TRAILER 0xdeadbeef
#define MAXFS_INODES 1024
#define MAXFS_BLOCKS 4096

typedef struct _superblock {
    int magic;
    int fsid;
    // inodes
    int ni_total;
    int ni_alloc;
    int ni_free;
    // blocks
    int nb_total;
    int nb_alloc;
    int nb_free;
    int ino_map[1024];
    int block_map[1024];
    int trailer;
} superblock;


superblock* init_fs(int fsid)
{
    superblock *sb = (superblock*) malloc(sizeof(superblock));
    sb->magic = SUPERMAGIC_HEAD;
    sb->fsid = fsid;
    sb->trailer = SUPERMAGIC_TRAILER;

    // they will be zero initially
    sb->ni_total = 0;
    sb->ni_alloc = 0;
    sb->ni_free = 0;
    sb->nb_total = 0;
    sb->nb_alloc = 0;
    sb->nb_free = 0;

    return sb;
}

superblock* mkfs(int fsid)
{
    return init_fs(fsid);
}

int write_sb(superblock *sb)
{
    int fd = open("myfs.bin", O_RDWR|O_CREAT, 0644);
    if (fd == -1) {
        perror("Unable to init rawfs");
    }
    pwrite(fd, (void*)sb, sizeof(sb), 0);
    close(fd);
}

int main()
{
    superblock *sb = mkfs(0xBABEBABE);
    write_sb(sb);
    //disp_superblock(sb);
    return 0;
}

