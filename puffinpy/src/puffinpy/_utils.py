
def bytecount_shorten(count) -> str:
    for unit in ['B', 'KB', 'MB', 'GB']:
        if count < 1024:
            return f'{count:.1f} {unit}'
        
        count /= 1024

    return f'{count:.1f} TB'
