# Apolloo

A platform for buyers and sellers.

## Features

- Buyer and seller interactions
- Database integration
- GUI for user interactions

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/20Vaibhavk/Apolloo.git
    cd Apolloo
    ```

2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up the database:
    ```sh
    psql -f apollodb.sql
    ```

## Usage

1. Run the application:
    ```sh
    python main.py
    ```

## Files

- `apollodb.sql`: SQL script to set up the database
- `buyer.py`: Buyer module
- `connect.py`: Database connection module
- `gui.py`: GUI implementation
- `main.py`: Main application script

## License

This project is licensed under the MIT License.
