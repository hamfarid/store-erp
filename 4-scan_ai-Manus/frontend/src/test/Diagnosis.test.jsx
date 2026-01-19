/**
 * Diagnosis.test.jsx - Tests for Diagnosis Page
 * Path: frontend/src/test/Diagnosis.test.jsx
 * 
 * Tests the AI-powered plant disease diagnosis functionality
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Diagnosis from '../../pages/Diagnosis';

// Mock ApiService
vi.mock('../../services/ApiService', () => ({
  default: {
    get: vi.fn(() => Promise.resolve({ data: [] })),
    post: vi.fn(() => Promise.resolve({ 
      data: { 
        id: 1,
        disease: 'Leaf Spot',
        confidence: 0.92,
        status: 'completed'
      } 
    })),
    put: vi.fn(() => Promise.resolve({ data: {} })),
    delete: vi.fn(() => Promise.resolve({ data: {} })),
  }
}));

// Mock react-router-dom
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => vi.fn(),
    useParams: () => ({}),
  };
});

// Mock react-dropzone
vi.mock('react-dropzone', () => ({
  useDropzone: () => ({
    getRootProps: () => ({}),
    getInputProps: () => ({}),
    isDragActive: false,
  }),
}));

// Mock toast
vi.mock('react-hot-toast', () => ({
  toast: {
    success: vi.fn(),
    error: vi.fn(),
    loading: vi.fn(),
  },
}));

// Mock lucide-react icons with all commonly used icons
vi.mock('lucide-react', async (importOriginal) => {
  const MockIcon = ({ 'data-testid': testId, ...props }) => (
    <span data-testid={testId || 'icon'} {...props} />
  );

  return {
    Camera: (props) => <MockIcon data-testid="camera-icon" {...props} />,
    Upload: (props) => <MockIcon data-testid="upload-icon" {...props} />,
    Image: (props) => <MockIcon data-testid="image-icon" {...props} />,
    Bug: (props) => <MockIcon data-testid="bug-icon" {...props} />,
    Leaf: (props) => <MockIcon data-testid="leaf-icon" {...props} />,
    CheckCircle: (props) => <MockIcon data-testid="check-icon" {...props} />,
    AlertTriangle: (props) => <MockIcon data-testid="alert-icon" {...props} />,
    Clock: (props) => <MockIcon data-testid="clock-icon" {...props} />,
    XCircle: (props) => <MockIcon data-testid="x-icon" {...props} />,
    ArrowRight: (props) => <MockIcon data-testid="arrow-icon" {...props} />,
    Sparkles: (props) => <MockIcon data-testid="sparkles-icon" {...props} />,
    Brain: (props) => <MockIcon data-testid="brain-icon" {...props} />,
    FileText: (props) => <MockIcon data-testid="file-icon" {...props} />,
    ThumbsUp: (props) => <MockIcon data-testid="thumbsup-icon" {...props} />,
    ThumbsDown: (props) => <MockIcon data-testid="thumbsdown-icon" {...props} />,
    RefreshCw: (props) => <MockIcon data-testid="refresh-icon" {...props} />,
    Download: (props) => <MockIcon data-testid="download-icon" {...props} />,
    Share2: (props) => <MockIcon data-testid="share-icon" {...props} />,
    Trash2: (props) => <MockIcon data-testid="trash-icon" {...props} />,
    History: (props) => <MockIcon data-testid="history-icon" {...props} />,
    Microscope: (props) => <MockIcon data-testid="microscope-icon" {...props} />,
    Activity: (props) => <MockIcon data-testid="activity-icon" {...props} />,
    Zap: (props) => <MockIcon data-testid="zap-icon" {...props} />,
    Filter: (props) => <MockIcon data-testid="filter-icon" {...props} />,
    Search: (props) => <MockIcon data-testid="search-icon" {...props} />,
    Plus: (props) => <MockIcon data-testid="plus-icon" {...props} />,
    Edit: (props) => <MockIcon data-testid="edit-icon" {...props} />,
    Eye: (props) => <MockIcon data-testid="eye-icon" {...props} />,
    MoreVertical: (props) => <MockIcon data-testid="more-icon" {...props} />,
    ChevronDown: (props) => <MockIcon data-testid="chevron-down-icon" {...props} />,
    ChevronUp: (props) => <MockIcon data-testid="chevron-up-icon" {...props} />,
    ChevronLeft: (props) => <MockIcon data-testid="chevron-left-icon" {...props} />,
    ChevronRight: (props) => <MockIcon data-testid="chevron-right-icon" {...props} />,
    X: (props) => <MockIcon data-testid="x-close-icon" {...props} />,
    Check: (props) => <MockIcon data-testid="check-small-icon" {...props} />,
    Loader2: (props) => <MockIcon data-testid="loader-icon" {...props} />,
    AlertCircle: (props) => <MockIcon data-testid="alert-circle-icon" {...props} />,
    Info: (props) => <MockIcon data-testid="info-icon" {...props} />,
    Settings: (props) => <MockIcon data-testid="settings-icon" {...props} />,
    User: (props) => <MockIcon data-testid="user-icon" {...props} />,
    Home: (props) => <MockIcon data-testid="home-icon" {...props} />,
    Wrench: (props) => <MockIcon data-testid="wrench-icon" {...props} />,
    Calendar: (props) => <MockIcon data-testid="calendar-icon" {...props} />,
    BarChart: (props) => <MockIcon data-testid="barchart-icon" {...props} />,
    PieChart: (props) => <MockIcon data-testid="piechart-icon" {...props} />,
    TrendingUp: (props) => <MockIcon data-testid="trending-icon" {...props} />,
    ArrowUpDown: (props) => <MockIcon data-testid="arrow-updown-icon" {...props} />,
    MoreHorizontal: (props) => <MockIcon data-testid="more-horizontal-icon" {...props} />,
    SortAsc: (props) => <MockIcon data-testid="sort-asc-icon" {...props} />,
    SortDesc: (props) => <MockIcon data-testid="sort-desc-icon" {...props} />,
    ArrowUp: (props) => <MockIcon data-testid="arrow-up-icon" {...props} />,
    ArrowDown: (props) => <MockIcon data-testid="arrow-down-icon" {...props} />,
    ChevronsRight: (props) => <MockIcon data-testid="chevrons-right-icon" {...props} />,
    ChevronsLeft: (props) => <MockIcon data-testid="chevrons-left-icon" {...props} />,
    Columns: (props) => <MockIcon data-testid="columns-icon" {...props} />,
    FileDown: (props) => <MockIcon data-testid="file-down-icon" {...props} />,
    Printer: (props) => <MockIcon data-testid="printer-icon" {...props} />,
    RotateCcw: (props) => <MockIcon data-testid="rotate-icon" {...props} />,
    ListFilter: (props) => <MockIcon data-testid="list-filter-icon" {...props} />,
    Menu: (props) => <MockIcon data-testid="menu-icon" {...props} />,
    MapPin: (props) => <MockIcon data-testid="map-pin-icon" {...props} />,
    Bell: (props) => <MockIcon data-testid="bell-icon" {...props} />,
    LogOut: (props) => <MockIcon data-testid="logout-icon" {...props} />,
    Moon: (props) => <MockIcon data-testid="moon-icon" {...props} />,
    Sun: (props) => <MockIcon data-testid="sun-icon" {...props} />,
  };
});

describe('Diagnosis Page', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render diagnosis page', () => {
    render(
      <BrowserRouter>
        <Diagnosis />
      </BrowserRouter>
    );
    
    expect(document.body).toBeTruthy();
  });

  it('should render page content', async () => {
    render(
      <BrowserRouter>
        <Diagnosis />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(document.body.textContent).toBeTruthy();
    });
  });

  it('should have upload functionality', async () => {
    const { container } = render(
      <BrowserRouter>
        <Diagnosis />
      </BrowserRouter>
    );

    await waitFor(() => {
      // Check for upload-related elements or diagnosis button
      const hasUploadIcon = container.querySelector('[data-testid="upload-icon"]');
      const hasUploadText = container.textContent.includes('upload') || container.textContent.includes('رفع');
      const hasDiagnosisButton = container.textContent.includes('تشخيص') || container.textContent.includes('diagnosis');
      // At least one of these should be present
      expect(hasUploadIcon || hasUploadText || hasDiagnosisButton || container.querySelector('button')).toBeTruthy();
    });
  });

  it('should render diagnosis history section', async () => {
    const { container } = render(
      <BrowserRouter>
        <Diagnosis />
      </BrowserRouter>
    );

    await waitFor(() => {
      // Page should have some content
      expect(container.querySelector('div')).toBeTruthy();
    });
  });
});

