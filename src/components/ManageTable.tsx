'use client';

import { Checkbox } from '@/components/ui/checkbox';
import { useState, useEffect, useMemo } from 'react';
import { Edit, Trash2 } from 'lucide-react';
import { Button } from './ui/button';
import Form from './EditeItem'; // Import your Form component

interface Invoice {
  item: string;
  category: string;
  weight: number;
  height: number;
  width: number;
  expiry: number;
  fragile: boolean;
}

const initialInvoicesData: Invoice[] = [
  {
    item: 'Screw Set',
    category: 'Materials',
    weight: 2.5,
    height: 10,
    width: 5,
    expiry: 365,
    fragile: false,
  },
  {
    item: 'Glass Vase',
    category: 'Household',
    weight: 1.8,
    height: 25,
    width: 15,
    expiry: 0,
    fragile: true,
  },
  {
    item: 'Wooden Box',
    category: 'Materials',
    weight: 5.0,
    height: 30,
    width: 20,
    expiry: 0,
    fragile: false,
  },
  {
    item: 'Electronics Kit',
    category: 'Electronics',
    weight: 3.2,
    height: 15,
    width: 12,
    expiry: 180,
    fragile: true,
  },
  {
    item: 'Food Container',
    category: 'Food',
    weight: 1.0,
    height: 8,
    width: 8,
    expiry: 90,
    fragile: false,
  },
];

export function ManageTable() {
  const [selectedInvoices, setSelectedInvoices] = useState<string[]>([]);
  const [sortConfig, setSortConfig] = useState<{
    key: keyof Invoice | null;
    direction: 'ascending' | 'descending' | null;
  }>({ key: null, direction: null });
  const [categoryFilter, setCategoryFilter] = useState<string>('all');
  const [weightFilter, setWeightFilter] = useState<string>('all');
  const [fragileFilter, setFragileFilter] = useState<string>('all');
  const [invoices, setInvoices] = useState<Invoice[]>(initialInvoicesData);
  const [editingInvoice, setEditingInvoice] = useState<Invoice | null>(null);
  const [isEditModalOpen, setIsEditModalOpen] = useState<boolean>(false);
  const [filteredInvoices, setFilteredInvoices] = useState<Invoice[]>(invoices);

  useEffect(() => {
    let newFilteredInvoices = [...invoices];

    // Category Filter
    if (categoryFilter !== 'all') {
      newFilteredInvoices = newFilteredInvoices.filter(
        (invoice) => invoice.category === categoryFilter,
      );
    }

    // Weight Filter
    if (weightFilter === 'light') {
      newFilteredInvoices = newFilteredInvoices.filter(
        (invoice) => invoice.weight < 2,
      );
    } else if (weightFilter === 'medium') {
      newFilteredInvoices = newFilteredInvoices.filter(
        (invoice) => invoice.weight >= 2 && invoice.weight <= 4,
      );
    } else if (weightFilter === 'heavy') {
      newFilteredInvoices = newFilteredInvoices.filter(
        (invoice) => invoice.weight > 4,
      );
    }

    // Fragile Filter
    if (fragileFilter !== 'all') {
      newFilteredInvoices = newFilteredInvoices.filter(
        (invoice) => invoice.fragile === (fragileFilter === 'yes'),
      );
    }

    setFilteredInvoices(newFilteredInvoices);
  }, [categoryFilter, weightFilter, fragileFilter, invoices]);

  const toggleInvoice = (invoice: string, checked: boolean) => {
    setSelectedInvoices((prev) =>
      checked ? [...prev, invoice] : prev.filter((i) => i !== invoice),
    );
  };

  const handleCategoryFilterChange = (
    event: React.ChangeEvent<HTMLSelectElement>,
  ) => {
    setCategoryFilter(event.target.value);
  };

  const handleWeightFilterChange = (
    event: React.ChangeEvent<HTMLSelectElement>,
  ) => {
    setWeightFilter(event.target.value);
  };

  const handleFragileFilterChange = (
    event: React.ChangeEvent<HTMLSelectElement>,
  ) => {
    setFragileFilter(event.target.value);
  };

  const requestSort = (key: keyof Invoice) => {
    let direction: 'ascending' | 'descending' = 'ascending';
    if (sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };

  const sortedInvoices = useMemo(() => {
    if (!sortConfig.key) {
      return filteredInvoices;
    }

    return [...filteredInvoices].sort((a, b) => {
      const key = sortConfig.key;
      if (key) {
        if (key === 'weight' || key === 'height' || key === 'width' || key === 'expiry') {
          const valueA = a[key];
          const valueB = b[key];
          if (valueA < valueB)
            return sortConfig.direction === 'ascending' ? -1 : 1;
          if (valueA > valueB)
            return sortConfig.direction === 'ascending' ? 1 : -1;
          return 0;
        } else if (key === 'fragile') {
          const valueA = a[key] ? 1 : 0;
          const valueB = b[key] ? 1 : 0;
          if (valueA < valueB)
            return sortConfig.direction === 'ascending' ? -1 : 1;
          if (valueA > valueB)
            return sortConfig.direction === 'ascending' ? 1 : -1;
          return 0;
        } else {
          // For string fields (item, category)
          const valueA = String(a[key]);
          const valueB = String(b[key]);
          if (valueA < valueB)
            return sortConfig.direction === 'ascending' ? -1 : 1;
          if (valueA > valueB)
            return sortConfig.direction === 'ascending' ? 1 : -1;
          return 0;
        }
      }
      return 0;
    });
  }, [filteredInvoices, sortConfig]);

  const handleEdit = (invoiceToEdit: Invoice) => {
    console.log('Edit clicked for:', invoiceToEdit.item);
    setEditingInvoice(invoiceToEdit);
    setIsEditModalOpen(true); // Open the edit modal
  };

  const handleSaveEdit = (editedData: any) => {
    const updatedInvoice: Invoice = {
      item: editedData.item,
      category: editedData.category,
      weight: editedData.weight,
      height: editedData.height,
      width: editedData.width,
      expiry: editedData.expiry,
      fragile: editedData.fragile,
    };
    setInvoices((prevInvoices) =>
      prevInvoices.map((inv) =>
        inv.item === editingInvoice?.item ? updatedInvoice : inv,
      ),
    );
    setIsEditModalOpen(false);
    setEditingInvoice(null);
  };

  const handleCancelEdit = () => {
    setIsEditModalOpen(false);
    setEditingInvoice(null);
  };

  const [isDeleteConfirmationVisible, setIsDeleteConfirmationVisible] =
    useState(false);
  const [invoiceToDelete, setInvoiceToDelete] = useState<Invoice | null>(null);

  const [notification, setNotification] = useState<{
    message: string;
    type: 'success' | 'error' | null;
  }>({
    message: '',
    type: null,
  });
  const [isNotificationVisible, setIsNotificationVisible] = useState(false);

  const showNotification = (message: string, type: 'success' | 'error') => {
    setNotification({ message, type });
    setIsNotificationVisible(true);
    // Automatically hide the notification after a few seconds
    setTimeout(() => {
      setIsNotificationVisible(false);
      setNotification({ message: '', type: null });
    }, 3000); // Adjust the duration as needed
  };

  const handleDelete = (invoiceToDelete: Invoice) => {
    console.log('Delete clicked for:', invoiceToDelete.item);
    setInvoiceToDelete(invoiceToDelete);
    setIsDeleteConfirmationVisible(true);
  };

  const confirmDelete = () => {
    if (invoiceToDelete) {
      setInvoices((prevInvoices) =>
        prevInvoices.filter((inv) => inv.item !== invoiceToDelete.item),
      );
      setSelectedInvoices((prevSelected) =>
        prevSelected.filter((inv) => inv !== invoiceToDelete.item),
      );
      showNotification(
        `Entry ${invoiceToDelete.item} deleted successfully!`,
        'success',
      );
      setIsDeleteConfirmationVisible(false);
      setInvoiceToDelete(null);
    }
  };

  const cancelDelete = () => {
    setIsDeleteConfirmationVisible(false);
    setInvoiceToDelete(null);
  };

  const uniqueCategories = [
    'all',
    ...Array.from(new Set(invoices.map((inv) => inv.category))).filter(Boolean),
  ];

  return (
    <div className="rounded-md bg-[#10111D] text-[#BFBFBF] font-bold p-1 mt-8 w-[90%]">
      <div className="w-full">
        <div className="grid grid-cols-[0.5fr_1fr_1fr_1fr_1fr_1fr_1fr_1fr_1fr] h-[50px]">
          <div className="flex items-center justify-center"></div>
          <div className="flex items-center font-medium justify-start">
            <button
              type="button"
              onClick={() => requestSort('item')}
              className="text-gray-400 hover:text-gray-200 flex items-center"
            >
              <span>Item</span>
            </button>
          </div>
          <div className="flex items-center font-medium justify-start">
            <div className="flex items-center gap-2">
              <span className="hidden xl:inline">Category</span>
              <select
                value={categoryFilter}
                onChange={handleCategoryFilterChange}
                className="bg-[#10111D] text-gray-400 border border-gray-700 rounded-md text-sm focus:outline-none"
              >
                {uniqueCategories.map((category) => (
                  <option key={category} value={category}>
                    {category ? category.charAt(0).toUpperCase() + category.slice(1) : ''}
                  </option>
                ))}
              </select>
            </div>
          </div>
          <div className="flex items-center justify-center font-medium">
            <div className="flex items-center gap-2">
              <span className="hidden xl:inline">Weight (kg)</span>
              <select
                value={weightFilter}
                onChange={handleWeightFilterChange}
                className="bg-[#10111D] text-gray-400 border border-gray-700 rounded-md text-sm focus:outline-none"
              >
                <option value="all">All</option>
                <option value="light">Light (&lt;2kg)</option>
                <option value="medium">Medium (2-4kg)</option>
                <option value="heavy">Heavy (&gt;4kg)</option>
              </select>
            </div>
          </div>
          <div className="flex items-center justify-center font-medium">
            <button
              type="button"
              onClick={() => requestSort('height')}
              className="text-gray-400 hover:text-gray-200 flex items-center"
            >
              <span>Height (cm)</span>
            </button>
          </div>
          <div className="flex items-center justify-center font-medium">
            <button
              type="button"
              onClick={() => requestSort('width')}
              className="text-gray-400 hover:text-gray-200 flex items-center"
            >
              <span>Width (cm)</span>
            </button>
          </div>
          <div className="flex items-center justify-center font-medium">
            <button
              type="button"
              onClick={() => requestSort('expiry')}
              className="text-gray-400 hover:text-gray-200 flex items-center"
            >
              <span>Expiry (days)</span>
            </button>
          </div>
          <div className="flex items-center justify-center font-medium">
            <div className="flex items-center gap-2">
              <span className="hidden xl:inline">Fragile</span>
              <select
                value={fragileFilter}
                onChange={handleFragileFilterChange}
                className="bg-[#10111D] text-gray-400 border border-gray-700 rounded-md text-sm focus:outline-none"
              >
                <option value="all">All</option>
                <option value="yes">Yes</option>
                <option value="no">No</option>
              </select>
            </div>
          </div>
          <div className="flex items-center justify-center font-medium">
            Actions
          </div>
        </div>

        <img
          src="/assets/svgs/SeparatorTable.svg"
          alt="Table Separator"
          className="w-full h-10"
        />
        <div className="overflow-y-auto h-[390px] [&::-webkit-scrollbar]:w-2 dark:[&::-webkit-scrollbar-track]:bg-[#10121E] dark:[&::-webkit-scrollbar-thumb]:bg-[#303137] overflow-x-hidden">
          {sortedInvoices.map((invoice) => (
            <div
              key={`${invoice.item}-${invoice.category}`}
              className="grid grid-cols-[0.5fr_1fr_1fr_1fr_1fr_1fr_1fr_1fr_1fr] h-[50px] border-b border-gray-800"
            >
              <div className="flex items-center justify-center">
                <Checkbox
                  checked={selectedInvoices.includes(invoice.item)}
                  onCheckedChange={(checked) =>
                    toggleInvoice(invoice.item, checked as boolean)
                  }
                  id={`invoice-${invoice.item}`}
                />
              </div>
              <div className="flex items-center truncate px-2" title={invoice.item}>
                {invoice.item}
              </div>
              <div className="flex items-center truncate px-2" title={invoice.category}>
                {invoice.category}
              </div>
              <div className="flex items-center justify-center truncate px-2">
                {invoice.weight} kg
              </div>
              <div className="flex items-center justify-center truncate px-2">
                {invoice.height} cm
              </div>
              <div className="flex items-center justify-center truncate px-2">
                {invoice.width} cm
              </div>
              <div className="flex items-center justify-center truncate px-2">
                {invoice.expiry > 0 ? `${invoice.expiry} days` : 'N/A'}
              </div>
              <div className="flex items-center justify-center truncate px-2">
                {invoice.fragile ? 'Yes' : 'No'}
              </div>
              <div className="flex items-center justify-center">
                <div className="flex space-x-2">
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => handleEdit(invoice)}
                  >
                    <Edit className="h-4 w-4" />
                    <span className="sr-only">Edit</span>
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => handleDelete(invoice)}
                  >
                    <Trash2 className="h-4 w-4" />
                    <span className="sr-only">Delete</span>
                  </Button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Edit Modal */}
        {isEditModalOpen && editingInvoice && (
          <div className="fixed top-0 left-0 w-full h-full bg-black/50 z-50 flex justify-center items-center">
            <div className="bg-[#1D2330] p-6 rounded-md w-[400px]">
              <h2 className="text-lg font-bold mb-4 text-white">
                Edit Item
              </h2>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Item Name</label>
                  <input
                    type="text"
                    value={editingInvoice.item}
                    onChange={(e) => setEditingInvoice({...editingInvoice, item: e.target.value})}
                    className="w-full bg-[#2A2F3D] text-white rounded-md px-3 py-2"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Category</label>
                  <select
                    value={editingInvoice.category}
                    onChange={(e) => setEditingInvoice({...editingInvoice, category: e.target.value})}
                    className="w-full bg-[#2A2F3D] text-white rounded-md px-3 py-2"
                  >
                    {uniqueCategories.filter(cat => cat !== 'all').map((category) => (
                      <option key={category} value={category}>
                        {category}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Weight (kg)</label>
                  <input
                    type="number"
                    value={editingInvoice.weight}
                    onChange={(e) => setEditingInvoice({...editingInvoice, weight: parseFloat(e.target.value)})}
                    className="w-full bg-[#2A2F3D] text-white rounded-md px-3 py-2"
                    step="0.1"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Height (cm)</label>
                  <input
                    type="number"
                    value={editingInvoice.height}
                    onChange={(e) => setEditingInvoice({...editingInvoice, height: parseInt(e.target.value)})}
                    className="w-full bg-[#2A2F3D] text-white rounded-md px-3 py-2"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Width (cm)</label>
                  <input
                    type="number"
                    value={editingInvoice.width}
                    onChange={(e) => setEditingInvoice({...editingInvoice, width: parseInt(e.target.value)})}
                    className="w-full bg-[#2A2F3D] text-white rounded-md px-3 py-2"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Expiry (days)</label>
                  <input
                    type="number"
                    value={editingInvoice.expiry}
                    onChange={(e) => setEditingInvoice({...editingInvoice, expiry: parseInt(e.target.value)})}
                    className="w-full bg-[#2A2F3D] text-white rounded-md px-3 py-2"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Fragile</label>
                  <select
                    value={editingInvoice.fragile ? 'yes' : 'no'}
                    onChange={(e) => setEditingInvoice({...editingInvoice, fragile: e.target.value === 'yes'})}
                    className="w-full bg-[#2A2F3D] text-white rounded-md px-3 py-2"
                  >
                    <option value="yes">Yes</option>
                    <option value="no">No</option>
                  </select>
                </div>
              </div>
              <div className="flex justify-end gap-2 mt-4">
                <Button onClick={handleCancelEdit} variant="ghost">
                  Cancel
                </Button>
                <Button onClick={() => handleSaveEdit(editingInvoice)}>
                  Save
                </Button>
              </div>
            </div>
          </div>
        )}

        {/* Notification */}
        {isNotificationVisible && notification.message && (
          <div
            className={`fixed bottom-4 right-4 bg-[#2E7D32] text-white p-4 rounded-md shadow-lg z-50 ${
              notification.type === 'error' ? 'bg-[#D32F2F]' : ''
            }`}
          >
            {notification.message}
          </div>
        )}

        {/* Delete Confirmation Modal */}
        {isDeleteConfirmationVisible && invoiceToDelete && (
          <div className="fixed top-0 left-0 w-full h-full bg-black/50 z-20 flex justify-center items-center">
            <div className="bg-[#1D2330] p-6 rounded-md">
              <h2 className="text-lg font-bold mb-4 text-white">
                Confirm Delete
              </h2>
              <p className="text-gray-400 mb-4">
                Are you sure you want to delete item{' '}
                <span className="font-bold text-white">
                  {invoiceToDelete.item}
                </span>
                ?
              </p>
              <div className="flex justify-end gap-2">
                <Button onClick={cancelDelete} variant="ghost">
                  Cancel
                </Button>
                <Button onClick={confirmDelete} variant="destructive">
                  Delete
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default ManageTable;
