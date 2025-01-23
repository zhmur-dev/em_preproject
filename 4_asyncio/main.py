import asyncio

from src import async_parser, sync_parser


if __name__ == '__main__':
    sync_elapsed = sync_parser.run()
    async_elapsed = asyncio.run(async_parser.run())
    total_diff = sync_elapsed - async_elapsed

    print(
        f'\nSync parser has completed its work within: '
        f'{sync_elapsed // 60} min {sync_elapsed % 60} sec.\n'
        f'Async parser has completed its work within: '
        f'{async_elapsed // 60} min {async_elapsed % 60} sec.\n'
        f'Total difference is: '
        f'{total_diff // 60} min {total_diff % 60} sec.\n'
    )
