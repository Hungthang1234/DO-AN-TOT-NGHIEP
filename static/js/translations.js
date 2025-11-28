// Language translations for House Price Prediction App
const translations = {
    en: {
        // Header
        title: "House Price Prediction & Analytics",
        subtitle: "Machine Learning powered real estate price prediction with advanced analytics",
        
        // Tab buttons
        tabSingle: "Single Prediction",
        tabBatch: "Batch Prediction",
        tabAnalytics: "Analytics Dashboard",
        tabVisualization: "Advanced Charts",
        
        // Theme toggle
        darkMode: "Dark Mode",
        lightMode: "Light Mode",
        
        // Language selector
        language: "Language",
        
        // Single Prediction Tab
        singleTitle: "Single Property Prediction",
        singleSubtitle: "Enter property details to get an instant price prediction",
        
        // Form labels
        propertyType: "Property Type",
        propertyTypePlaceholder: "Select property type",
        area: "Area (sqm)",
        areaPlaceholder: "Enter area in square meters",
        location: "Location",
        locationPlaceholder: "Enter location/address",
        bedrooms: "Bedrooms",
        bedroomsPlaceholder: "Number of bedrooms",
        bathrooms: "Bathrooms",
        bathroomsPlaceholder: "Number of bathrooms",
        yearBuilt: "Year Built",
        yearBuiltPlaceholder: "Year of construction",
        floorLevel: "Floor Level",
        floorLevelPlaceholder: "Floor number",
        
        // Property types
        ptApartment: "Apartment",
        ptCondo: "Condo",
        ptHDB: "HDB",
        ptLanded: "Landed",
        ptExecutiveCondo: "Executive Condo",
        
        // Buttons
        predict: "Predict Price",
        predictBatch: "Process Batch",
        loadCharts: "Load Charts Now",
        tryAgain: "Try Again",
        downloadTemplate: "Download Template",
        uploadFile: "Upload CSV File",
        
        // Results
        predictedPrice: "Predicted Price",
        predictionSuccess: "Prediction completed successfully!",
        processingPrediction: "Processing prediction...",
        processingBatch: "Processing batch predictions...",
        
        // Batch Prediction Tab
        batchTitle: "Batch Prediction",
        batchSubtitle: "Upload a CSV file with multiple properties for batch prediction.",
        batchInstructions: "Upload your CSV file containing property data. The file should include columns:",
        batchRequiredCols: "Required columns:",
        batchOptionalCols: "Optional columns:",
        batchSuccess: "Batch prediction completed successfully!",
        batchTotalProcessed: "Total properties processed",
        batchAvgPrice: "Average predicted price",
        batchPriceRange: "Price range",
        batchDistribution: "Batch Prediction Distribution",
        
        // Analytics Dashboard Tab
        analyticsTitle: "Real Estate Market Analytics",
        analyticsSubtitle: "Comprehensive market insights and trends",
        overviewTitle: "Market Overview",
        totalProperties: "Total Properties",
        avgPrice: "Average Price",
        avgArea: "Average Area",
        pricePerSqm: "Price per sqm",
        
        // Charts
        priceDistribution: "Price Distribution",
        propertyTypeDistribution: "Property Type Distribution",
        priceVsArea: "Price vs Area Analysis",
        topLocations: "Top 10 Locations by Average Price",
        priceByPropertyType: "Average Price by Property Type",
        monthlyTrend: "Monthly Price Trend",
        
        // Advanced Charts Tab
        vizWelcome: "Welcome to Advanced Charts",
        vizDescription: "Explore comprehensive real estate market visualizations and insights",
        vizLoading: "Loading visualizations...",
        vizError: "Failed to load charts. Please try again.",
        
        // Chart titles
        chartOverview: "Market Overview Statistics",
        chartPriceTrend: "Historical Price Trend",
        chartPropertyDist: "Property Type Distribution",
        chartPriceRange: "Price Range Distribution",
        chartAreaDist: "Area Distribution",
        chartSeasonal: "Seasonal Price Patterns",
        chartTopCities: "Top Cities by Average Price",
        chartPriceByType: "Price Trends by Property Type",
        
        // Filter labels
        filterCountry: "Country",
        filterSelectCountry: "Select country",
        
        // Messages
        errorOccurred: "An error occurred",
        noDataAvailable: "No data available",
        loadingData: "Loading data...",
        selectFile: "Please select a file",
        fillAllFields: "Please fill in all required fields",
        
        // Units
        million: "M",
        thousand: "K",
        sqm: "sqm",
        properties: "properties",
        
        // Time
        month: "Month",
        year: "Year",
        
        // Footer/Info
        poweredBy: "Powered by Machine Learning",
        dataSource: "Data Source",
        lastUpdated: "Last Updated",
        
        // Version Banner
        versionBadge: "API VERSION - NEW",
        versionDescription: "Singapore HDB System with Property Type • 978K records • Enhanced APIs",
        switchVersion: "Switch Version",
        
        // Model Info
        activeModel: "Active Model",
        performance: "Performance",
        trainedOn: "Trained On",
        
        // Additional UI
        clearResults: "Clear Results",
        clickToUpload: "Click to upload CSV file",
        csvShouldContain: "CSV should contain columns",
        downloadInfo: "Download template above for correct format",
        
        // Countries
        singapore: "Singapore",
        australia: "Australia",
        usa: "USA",
        allCountries: "All Countries",
        selectCountry: "Select Country",
        selectCountryFirst: "Select Country First...",
        
        // Property Type Options
        oneRoom: "1 ROOM",
        twoRoom: "2 ROOM",
        threeRoom: "3 ROOM",
        fourRoom: "4 ROOM",
        fiveRoom: "5 ROOM",
        executive: "EXECUTIVE",
        multiGen: "MULTI-GENERATION"
    },
    
    vi: {
        // Header
        title: "Dự Đoán Giá Bất Động Sản & Phân Tích",
        subtitle: "Dự đoán giá bất động sản với Machine Learning và phân tích nâng cao",
        
        // Tab buttons
        tabSingle: "Dự Đoán Đơn",
        tabBatch: "Dự Đoán Hàng Loạt",
        tabAnalytics: "Bảng Phân Tích",
        tabVisualization: "Biểu Đồ Nâng Cao",
        
        // Theme toggle
        darkMode: "Chế Độ Tối",
        lightMode: "Chế Độ Sáng",
        
        // Language selector
        language: "Ngôn Ngữ",
        
        // Single Prediction Tab
        singleTitle: "Dự Đoán Giá Bất Động Sản",
        singleSubtitle: "Nhập thông tin bất động sản để nhận dự đoán giá ngay lập tức",
        
        // Form labels
        propertyType: "Loại Bất Động Sản",
        propertyTypePlaceholder: "Chọn loại bất động sản",
        area: "Diện Tích (m²)",
        areaPlaceholder: "Nhập diện tích (m²)",
        location: "Vị Trí",
        locationPlaceholder: "Nhập địa chỉ/vị trí",
        bedrooms: "Phòng Ngủ",
        bedroomsPlaceholder: "Số phòng ngủ",
        bathrooms: "Phòng Tắm",
        bathroomsPlaceholder: "Số phòng tắm",
        yearBuilt: "Năm Xây Dựng",
        yearBuiltPlaceholder: "Năm xây dựng",
        floorLevel: "Tầng",
        floorLevelPlaceholder: "Số tầng",
        
        // Property types
        ptApartment: "Chung Cư",
        ptCondo: "Căn Hộ Cao Cấp",
        ptHDB: "HDB",
        ptLanded: "Nhà Đất",
        ptExecutiveCondo: "Căn Hộ Hành Chính",
        
        // Buttons
        predict: "Dự Đoán Giá",
        predictBatch: "Xử Lý Hàng Loạt",
        loadCharts: "Tải Biểu Đồ",
        tryAgain: "Thử Lại",
        downloadTemplate: "Tải Mẫu",
        uploadFile: "Tải Lên File CSV",
        
        // Results
        predictedPrice: "Giá Dự Đoán",
        predictionSuccess: "Dự đoán hoàn tất thành công!",
        processingPrediction: "Đang xử lý dự đoán...",
        processingBatch: "Đang xử lý dự đoán hàng loạt...",
        
        // Batch Prediction Tab
        batchTitle: "Dự Đoán Hàng Loạt",
        batchSubtitle: "Tải lên file CSV với nhiều bất động sản để dự đoán hàng loạt.",
        batchInstructions: "Tải lên file CSV chứa dữ liệu bất động sản. File cần có các cột:",
        batchRequiredCols: "Cột bắt buộc:",
        batchOptionalCols: "Cột tùy chọn:",
        batchSuccess: "Dự đoán hàng loạt hoàn tất thành công!",
        batchTotalProcessed: "Tổng số bất động sản đã xử lý",
        batchAvgPrice: "Giá trung bình dự đoán",
        batchPriceRange: "Khoảng giá",
        batchDistribution: "Phân Phối Giá Dự Đoán Hàng Loạt",
        
        // Analytics Dashboard Tab
        analyticsTitle: "Phân Tích Thị Trường Bất Động Sản",
        analyticsSubtitle: "Thông tin chi tiết và xu hướng thị trường",
        overviewTitle: "Tổng Quan Thị Trường",
        totalProperties: "Tổng Số BĐS",
        avgPrice: "Giá Trung Bình",
        avgArea: "Diện Tích TB",
        pricePerSqm: "Giá/m²",
        
        // Charts
        priceDistribution: "Phân Phối Giá",
        propertyTypeDistribution: "Phân Phối Loại BĐS",
        priceVsArea: "Phân Tích Giá và Diện Tích",
        topLocations: "Top 10 Vị Trí Theo Giá Trung Bình",
        priceByPropertyType: "Giá Trung Bình Theo Loại BĐS",
        monthlyTrend: "Xu Hướng Giá Theo Tháng",
        
        // Advanced Charts Tab
        vizWelcome: "Chào Mừng Đến Biểu Đồ Nâng Cao",
        vizDescription: "Khám phá trực quan hóa và thông tin chi tiết về thị trường bất động sản",
        vizLoading: "Đang tải biểu đồ...",
        vizError: "Không thể tải biểu đồ. Vui lòng thử lại.",
        
        // Chart titles
        chartOverview: "Thống Kê Tổng Quan Thị Trường",
        chartPriceTrend: "Xu Hướng Giá Lịch Sử",
        chartPropertyDist: "Phân Phối Loại BĐS",
        chartPriceRange: "Phân Phối Khoảng Giá",
        chartAreaDist: "Phân Phối Diện Tích",
        chartSeasonal: "Mô Hình Giá Theo Mùa",
        chartTopCities: "Thành Phố Có Giá Cao Nhất",
        chartPriceByType: "Xu Hướng Giá Theo Loại BĐS",
        
        // Filter labels
        filterCountry: "Quốc Gia",
        filterSelectCountry: "Chọn quốc gia",
        
        // Messages
        errorOccurred: "Đã xảy ra lỗi",
        noDataAvailable: "Không có dữ liệu",
        loadingData: "Đang tải dữ liệu...",
        selectFile: "Vui lòng chọn file",
        fillAllFields: "Vui lòng điền đầy đủ thông tin bắt buộc",
        
        // Units
        million: "Tr",
        thousand: "N",
        sqm: "m²",
        properties: "BĐS",
        
        // Time
        month: "Tháng",
        year: "Năm",
        
        // Footer/Info
        poweredBy: "Sử dụng Machine Learning",
        dataSource: "Nguồn Dữ Liệu",
        lastUpdated: "Cập Nhật Lần Cuối",
        
        // Version Banner
        versionBadge: "PHIÊN BẢN API - MỚI",
        versionDescription: "Hệ Thống HDB Singapore với Property Type • 978K bản ghi • APIs Nâng Cao",
        switchVersion: "Đổi Phiên Bản",
        
        // Model Info
        activeModel: "Model Đang Dùng",
        performance: "Hiệu Suất",
        trainedOn: "Huấn Luyện Trên",
        
        // Additional UI
        clearResults: "Xóa Kết Quả",
        clickToUpload: "Nhấp để tải lên file CSV",
        csvShouldContain: "CSV cần chứa các cột",
        downloadInfo: "Tải mẫu ở trên để có định dạng đúng",
        
        // Countries
        singapore: "Singapore",
        australia: "Úc",
        usa: "Mỹ",
        allCountries: "Tất Cả Quốc Gia",
        selectCountry: "Chọn Quốc Gia",
        selectCountryFirst: "Chọn Quốc Gia Trước...",
        
        // Property Type Options
        oneRoom: "1 PHÒNG",
        twoRoom: "2 PHÒNG",
        threeRoom: "3 PHÒNG",
        fourRoom: "4 PHÒNG",
        fiveRoom: "5 PHÒNG",
        executive: "CAO CẤP",
        multiGen: "ĐA THẾ HỆ"
    }
};

// Language manager
class LanguageManager {
    constructor() {
        this.currentLang = localStorage.getItem('preferredLanguage') || 'en';
        this.init();
    }
    
    init() {
        this.updateLanguage(this.currentLang);
    }
    
    updateLanguage(lang) {
        this.currentLang = lang;
        localStorage.setItem('preferredLanguage', lang);
        document.documentElement.lang = lang;
        
        // Update all elements with data-i18n attribute
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.getTranslation(key);
            
            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                if (element.placeholder !== undefined) {
                    element.placeholder = translation;
                }
            } else if (element.tagName === 'OPTION') {
                element.textContent = translation;
            } else {
                element.innerHTML = translation;
            }
        });
        
        // Update elements with data-i18n-html (preserve HTML)
        document.querySelectorAll('[data-i18n-html]').forEach(element => {
            const key = element.getAttribute('data-i18n-html');
            element.innerHTML = this.getTranslation(key);
        });
        
        // Update title
        document.title = this.getTranslation('title');
        
        // Dispatch event for custom updates
        window.dispatchEvent(new CustomEvent('languageChanged', { detail: { lang: lang } }));
    }
    
    getTranslation(key) {
        return translations[this.currentLang]?.[key] || translations['en']?.[key] || key;
    }
    
    toggle() {
        const newLang = this.currentLang === 'en' ? 'vi' : 'en';
        this.updateLanguage(newLang);
        return newLang;
    }
    
    getCurrentLang() {
        return this.currentLang;
    }
}

// Initialize language manager
const langManager = new LanguageManager();

// Utility function for getting translations in JavaScript
function t(key) {
    return langManager.getTranslation(key);
}
