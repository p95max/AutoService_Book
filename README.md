# 🚗 AutoService Book

**AutoService Book** is your reliable assistant for tracking and managing your car’s service history. This web application, built as a portfolio project, showcases skills in Django development, database management, and creating user-friendly interfaces.

## About

AutoService Book is designed for car owners who want to:
- Keep detailed records of all maintenance and repair work.
- Store information about oil changes, inspections, repairs, and fuel expenses.
- View complete service and expense history in one convenient place.
- Stay on top of upcoming services and monitor costs.

With a clean and intuitive interface, you can easily:
- Add and edit service records.
- Manage fuel expenses and track consumption.
- Record purchased and installed car parts.
- View service history for each vehicle.
- Analyze average fuel consumption and remaining fuel.
- Manage multiple cars from a personal dashboard.
- Export data to CSV tables.

AutoService Book brings organization, transparency, and ease to your car ownership experience.

## Features

- 🛠️ **Track Service History and Car Parts**: Add, edit, and delete service and part records.
- 🚗 **Manage Vehicles**: Keep track of multiple cars with details (brand, model, year, mileage, VIN).
- 🔋 **Monitor Fuel Expenses**: Record fuel purchases, calculate distances, and track costs.
- ⛽ **Check Fuel Levels and Consumption**: Automatically calculate remaining fuel and average consumption.
- 📊 **Analyze Expenses**: View all expenses and service history in one place.
- 📥 **CSV Export**: Download service, fuel, part, and other expense data as CSV files.
- 🌗 **Dark/Light Theme Switcher**: Toggle between light and dark themes for a comfortable experience.

## Tech Stack

- **Backend**: Django 4.2, Python 3.13
- **Frontend**: Bootstrap 5 (via `crispy-bootstrap5`), HTML, CSS, JavaScript
- **Database**: SQLite (with easy switch to PostgreSQL)
- **Authentication**: `django-allauth` for email-based login
- **Caching**: Django Cache Framework for optimized queries
- **Additional**: Django signals for automatic mileage and fuel updates, CSV export functionality

## Usage

1. **Sign Up/Login**: Register or log in via email using `django-allauth`.
2. **Add Vehicles**: Go to the "Autos" section to add cars (brand, model, year, mileage, VIN).
3. **Manage Records**:
   - Add service records, fuel expenses, car parts, or other expenses.
   - View detailed history and analytics for each car.
   - Export data to CSV for offline use.
4. **Monitor Fuel**: Check remaining fuel and average consumption on the dashboard.
5. **Toggle Themes**: Switch between dark and light themes for a better experience.

## Portfolio Notes

This project was built to demonstrate:
- Proficiency in Django, including models, views, forms, and signals.
- Database design and management with SQLite.
- User authentication and security with `django-allauth`.
- Responsive UI with Bootstrap 5 and `crispy-forms`.
- Performance optimization using caching.
- Data export functionality with CSV.

Feel free to explore the code, test the app, or provide feedback!


## Contributing

This is a portfolio project, but suggestions or feedback are welcome! Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.