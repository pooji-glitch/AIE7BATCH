# AI Credit Risk & Score Analyzer - Frontend

A modern, responsive React frontend for the AI Credit Risk & Score Analyzer application. This frontend provides an intuitive interface for credit risk assessment, data visualization, and comprehensive reporting.

## 🚀 Features

### 📊 Dashboard
- Real-time analytics and key performance indicators
- Interactive charts and visualizations
- Recent activity feed
- Risk distribution overview
- Credit score trends

### 🔍 Credit Analysis
- Comprehensive credit application forms
- AI-powered risk assessment
- Real-time scoring and recommendations
- Detailed factor analysis
- Confidence level indicators

### 📋 Data Viewer
- Advanced data table with sorting and filtering
- Search functionality across applications
- Expandable row details
- Export capabilities
- Bulk operations

### 📈 Reports
- Multiple report types (Credit Analysis, Approval Rates, Risk Assessment, Performance Metrics)
- Interactive charts and graphs
- Export to PDF and Excel
- Date range filtering
- Key insights and recommendations

## 🛠️ Technology Stack

- **React 18** - Modern React with hooks and functional components
- **React Router** - Client-side routing
- **Tailwind CSS** - Utility-first CSS framework
- **Chart.js** - Interactive charts and graphs
- **React Hook Form** - Form handling and validation
- **Axios** - HTTP client for API communication
- **Lucide React** - Beautiful icons
- **React Hot Toast** - Toast notifications

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   REACT_APP_API_URL=http://localhost:5000/api
   REACT_APP_ENVIRONMENT=development
   ```

4. **Start the development server**
   ```bash
   npm start
   ```

The application will be available at `http://localhost:3000`

## 🏗️ Project Structure

```
frontend/
├── public/
│   ├── index.html          # Main HTML file
│   └── manifest.json       # PWA manifest
├── src/
│   ├── components/         # Reusable components
│   │   └── Navbar.js       # Navigation component
│   ├── pages/             # Page components
│   │   ├── Dashboard.js    # Dashboard page
│   │   ├── CreditAnalysis.js # Credit analysis page
│   │   ├── DataViewer.js   # Data viewer page
│   │   └── Reports.js      # Reports page
│   ├── styles/            # CSS styles
│   │   └── App.css        # Main stylesheet
│   ├── utils/             # Utility functions
│   │   └── api.js         # API utilities
│   ├── App.js             # Main App component
│   └── index.js           # Application entry point
├── package.json           # Dependencies and scripts
└── tailwind.config.js     # Tailwind configuration
```

## 🎨 Design System

### Color Palette
- **Primary Blue**: `#3B82F6` - Main brand color
- **Success Green**: `#22C55E` - Positive actions and approvals
- **Warning Yellow**: `#F59E0B` - Medium risk and warnings
- **Danger Red**: `#EF4444` - High risk and errors
- **Neutral Gray**: `#6B7280` - Text and borders

### Typography
- **Font Family**: Inter (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700
- **Responsive**: Scales appropriately across devices

### Components
- **Cards**: Consistent shadow and border radius
- **Buttons**: Multiple variants (primary, secondary, success, danger)
- **Forms**: Clean input styling with focus states
- **Tables**: Sortable columns with hover effects
- **Charts**: Interactive visualizations with consistent theming

## 🔧 Available Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm eject` - Eject from Create React App

## 📱 Responsive Design

The application is fully responsive and optimized for:
- **Desktop**: 1024px and above
- **Tablet**: 768px to 1023px
- **Mobile**: 320px to 767px

## 🔌 API Integration

The frontend integrates with the backend API through the `api.js` utility file, which includes:

- **Credit Analysis API**: Risk assessment and scoring
- **Dashboard API**: Statistics and activity data
- **Data Management API**: CRUD operations for applications
- **Reports API**: Report generation and export
- **Market Data API**: Financial market information
- **AI Model API**: Model performance and status

## 🚀 Deployment

### Production Build
```bash
npm run build
```

### Environment Variables for Production
```env
REACT_APP_API_URL=https://your-api-domain.com/api
REACT_APP_ENVIRONMENT=production
```

### Deployment Platforms
- **Netlify**: Drag and drop the `build` folder
- **Vercel**: Connect your GitHub repository
- **AWS S3**: Upload build files to S3 bucket
- **Docker**: Use the provided Dockerfile

## 🧪 Testing

```bash
# Run all tests
npm test

# Run tests with coverage
npm test -- --coverage

# Run tests in watch mode
npm test -- --watch
```

## 📊 Performance Optimization

- **Code Splitting**: Routes are lazy-loaded
- **Image Optimization**: Optimized images and icons
- **Bundle Analysis**: Use `npm run build -- --analyze`
- **Caching**: Proper cache headers for static assets
- **Compression**: Gzip compression enabled

## 🔒 Security

- **HTTPS**: All API calls use HTTPS in production
- **Input Validation**: Form validation on client and server
- **XSS Protection**: React's built-in XSS protection
- **CSRF Protection**: Token-based CSRF protection
- **Content Security Policy**: CSP headers configured

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔄 Version History

- **v1.0.0** - Initial release with core features
- **v1.1.0** - Added advanced reporting capabilities
- **v1.2.0** - Enhanced data visualization and export features
- **v1.3.0** - Improved performance and mobile responsiveness

---

Built with ❤️ by the AIE7 Credit Risk Analyzer Team
