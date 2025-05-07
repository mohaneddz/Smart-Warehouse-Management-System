'use client';

import { Checkbox } from '@/components/ui/checkbox';
import { useState, useEffect, useMemo } from 'react';
import { Edit, Trash2 } from 'lucide-react';
import { Button } from './ui/button';
import Form from './EditeItem'; // Import your Form component

interface Invoice {
  invoice: string;
  paymentStatus: string;
  totalAmount: string;
  paymentMethod: string;
}

const initialInvoicesData: Invoice[] = [
  {
    invoice: 'INV001',
    paymentStatus: 'Paid',
    totalAmount: '$250.00',
    paymentMethod: 'Credit Card',
  },
  {
    invoice: 'INV002',
    paymentStatus: 'Pending',
    totalAmount: '$150.00',
    paymentMethod: 'PayPal',
  },
  {
    invoice: 'INV003',
    paymentStatus: 'Unpaid',
    totalAmount: '$350.00',
    paymentMethod: 'Bank Transfer',
  },
  {
    invoice: 'INV004',
    paymentStatus: 'Paid',
    totalAmount: '$450.00',
    paymentMethod: 'Credit Card',
  },
  {
    invoice: 'INV005',
    paymentStatus: 'Paid',
    totalAmount: '$550.00',
    paymentMethod: 'PayPal',
  },
  {
    invoice: 'INV006',
    paymentStatus: 'Pending',
    totalAmount: '$200.00',
    paymentMethod: 'Bank Transfer',
  },
  {
    invoice: 'INV007',
    paymentStatus: 'Unpaid',
    totalAmount: '$300.00',
    paymentMethod: 'Credit Card',
  },
  {
    invoice: 'INV008',
    paymentStatus: 'Paid',
    totalAmount: '$650.00',
    paymentMethod: 'Credit Card',
  },
  {
    invoice: 'INV009',
    paymentStatus: 'Pending',
    totalAmount: '$750.00',
    paymentMethod: 'PayPal',
  },
  {
    invoice: 'INV010',
    paymentStatus: 'Unpaid',
    totalAmount: '$850.00',
    paymentMethod: 'Bank Transfer',
  },
];

export function ManageTable() {
  const [selectedInvoices, setSelectedInvoices] = useState<string[]>([]);
  const [sortConfig, setSortConfig] = useState<{
    key: keyof Invoice | null;
    direction: 'ascending' | 'descending' | null;
  }>({ key: null, direction: null });
  const [amountFilter, setAmountFilter] = useState<string>('all');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [methodFilter, setMethodFilter] = useState<string>('all');
  const [invoices, setInvoices] = useState<Invoice[]>(initialInvoicesData);
  const [editingInvoice, setEditingInvoice] = useState<Invoice | null>(null);
  const [isEditModalOpen, setIsEditModalOpen] = useState<boolean>(false);
  const [filteredInvoices, setFilteredInvoices] = useState<Invoice[]>(invoices);

  useEffect(() => {
    let newFilteredInvoices = [...invoices];

    // Amount Filter
    if (amountFilter === 'under200') {
      newFilteredInvoices = newFilteredInvoices.filter(
        (invoice) => parseFloat(invoice.totalAmount.replace('$', '')) < 200,
      );
    } else if (amountFilter === '200to500') {
      newFilteredInvoices = newFilteredInvoices.filter((invoice) => {
        const amount = parseFloat(invoice.totalAmount.replace('$', ''));
        return amount >= 200 && amount <= 500;
      });
    } else if (amountFilter === 'over500') {
      newFilteredInvoices = newFilteredInvoices.filter(
        (invoice) => parseFloat(invoice.totalAmount.replace('$', '')) > 500,
      );
    }

    // Status Filter
    if (statusFilter !== 'all') {
      newFilteredInvoices = newFilteredInvoices.filter(
        (invoice) => invoice.paymentStatus === statusFilter,
      );
    }

    // Method Filter
    if (methodFilter !== 'all') {
      newFilteredInvoices = newFilteredInvoices.filter(
        (invoice) => invoice.paymentMethod === methodFilter,
      );
    }

    setFilteredInvoices(newFilteredInvoices);
  }, [amountFilter, statusFilter, methodFilter, invoices]);

  const toggleInvoice = (invoice: string, checked: boolean) => {
    setSelectedInvoices((prev) =>
      checked ? [...prev, invoice] : prev.filter((i) => i !== invoice),
    );
  };

  const handleCheckboxChange = (
    invoice: string,
    event: React.ChangeEvent<HTMLInputElement>,
  ) => {
    toggleInvoice(invoice, event.target.checked);
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
        if (key === 'totalAmount') {
          const amountA = parseFloat(a[key].replace('$', ''));
          const amountB = parseFloat(b[key].replace('$', ''));
          if (amountA < amountB)
            return sortConfig.direction === 'ascending' ? -1 : 1;
          if (amountA > amountB)
            return sortConfig.direction === 'ascending' ? 1 : -1;
          return 0;
        } else {
          if (a[key] < b[key])
            return sortConfig.direction === 'ascending' ? -1 : 1;
          if (a[key] > b[key])
            return sortConfig.direction === 'ascending' ? 1 : -1;
          return 0;
        }
      }
      return 0;
    });
  }, [filteredInvoices, sortConfig]);

  const handleAmountFilterChange = (
    event: React.ChangeEvent<HTMLSelectElement>,
  ) => {
    setAmountFilter(event.target.value);
  };

  const handleStatusFilterChange = (
    event: React.ChangeEvent<HTMLSelectElement>,
  ) => {
    setStatusFilter(event.target.value);
  };

  const handleMethodFilterChange = (
    event: React.ChangeEvent<HTMLSelectElement>,
  ) => {
    setMethodFilter(event.target.value);
  };

  const handleEdit = (invoiceToEdit: Invoice) => {
    console.log('Edit clicked for:', invoiceToEdit.invoice);
    setEditingInvoice(invoiceToEdit);
    setIsEditModalOpen(true); // Open the edit modal
  };

  const handleSaveEdit = (editedData: Invoice) => {
    console.log('Saving edited data:', editedData);
    setInvoices((prevInvoices) =>
      prevInvoices.map((inv) =>
        inv.invoice === editedData.invoice ? editedData : inv,
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
    console.log('Delete clicked for:', invoiceToDelete.invoice);
    setInvoiceToDelete(invoiceToDelete);
    setIsDeleteConfirmationVisible(true);
  };

  const confirmDelete = () => {
    if (invoiceToDelete) {
      setInvoices((prevInvoices) =>
        prevInvoices.filter((inv) => inv.invoice !== invoiceToDelete.invoice),
      );
      setSelectedInvoices((prevSelected) =>
        prevSelected.filter((inv) => inv !== invoiceToDelete.invoice),
      );
      showNotification(
        `Invoice ${invoiceToDelete.invoice} deleted successfully!`,
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

  const uniqueStatuses = [
    'all',
    ...Array.from(new Set(invoices.map((inv) => inv.paymentStatus))),
  ];
  const uniqueMethods = [
    'all',
    ...Array.from(new Set(invoices.map((inv) => inv.paymentMethod))),
  ];

  return (
    <div className="rounded-md bg-[#10111D] text-[#BFBFBF] font-bold p-1">
      <div className="w-full relative">
        <div className="grid grid-cols-[0.5fr_1.5fr_1.5fr_1.5fr_1fr_1fr_1fr] h-[50px] ">
          <div className="flex items-center justify-center"></div>
          <div className="flex items-center font-medium justify-start">
            <button
              type="button"
              onClick={() => requestSort('invoice')}
              className="text-gray-400 hover:text-gray-200 flex items-center"
            >
              <span>Invoice</span>
            </button>
          </div>
          <div className="flex items-center font-medium justify-start">
            <div className="flex items-center gap-2">
              <span>Status</span>
              <select
                value={statusFilter}
                onChange={handleStatusFilterChange}
                className="bg-[#10111D] text-gray-400 border border-gray-700 rounded-md text-sm focus:outline-none"
              >
                {uniqueStatuses.map((status) => (
                  <option key={status} value={status}>
                    {status.charAt(0).toUpperCase() + status.slice(1)}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="flex items-center font-medium justify-start">
            <div className="flex items-center gap-2">
              <span>Method</span>
              <select
                value={methodFilter}
                onChange={handleMethodFilterChange}
                className="bg-[#10111D] text-gray-400 border w-[55%] border-gray-700 rounded-md text-sm focus:outline-none"
              >
                {uniqueMethods.map((method) => (
                  <option key={method} value={method}>
                    {method}
                  </option>
                ))}
              </select>
            </div>
          </div>
          <div className="flex items-center justify-center font-medium">
            <div className="flex items-center gap-2">
              <span>Amount</span>
              <select
                value={amountFilter}
                onChange={handleAmountFilterChange}
                className="bg-[#10111D] text-gray-400 border border-gray-700 rounded-md text-sm focus:outline-none"
              >
                <option value="all">All</option>
                <option value="under200">Under $200</option>
                <option value="200to500">$200 - $500</option>
                <option value="over500">Over $500</option>
              </select>
            </div>
          </div>

          <div className="flex items-center justify-center font-medium">
            Actions
          </div>
        </div>

        {/* Table Content */}
        <img
          src="/assets/svgs/SeparatorTable.svg"
          alt="Chart"
          className="w-full h-10"
        />
        <div className="overflow-y-auto h-[390px] [&::-webkit-scrollbar]:w-2 dark:[&::-webkit-scrollbar-track]:bg-[#10121E] dark:[&::-webkit-scrollbar-thumb]:bg-[#303137] overflow-x-hidden">
          {sortedInvoices.map((invoice) => (
            <div
              key={invoice.invoice}
              className="grid grid-cols-[0.5fr_1.5fr_1.5fr_1.5fr_1fr_1fr_1fr] h-[65px] border-b border-gray-800 "
            >
              <div className="flex items-center justify-center">
                <Checkbox
                  checked={selectedInvoices.includes(invoice.invoice)}
                  onCheckedChange={(checked) =>
                    toggleInvoice(invoice.invoice, checked)
                  }
                  id={`invoice-${invoice.invoice}`}
                />
              </div>
              <div className="flex items-center">{invoice.invoice}</div>
              <div className="flex items-center">{invoice.paymentStatus}</div>
              <div className="flex items-center">{invoice.paymentMethod}</div>
              <div className="flex items-center justify-center w-30 m-4">
                {invoice.totalAmount}
              </div>
              <div className="flex items-center justify-center p-4 ">
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
          <div className="absolute top-0 left-0 w-full h-full z-50 bg-black/50 flex justify-center items-center">
            <div className="bg-[#05060fe8] p-6 rounded-md">
              <h2 className="text-lg font-bold mb-4 text-white">
                Edit Items :
              </h2>
              <Form
                initialFormData={{
                  type: '', // You might need to adjust how you map Invoice to Form data
                  name: editingInvoice.invoice,
                  quantity: 1, // Add relevant mapping if needed
                  weight: 1,
                  expiry: 1,
                  fragility: 1,
                  width: 1,
                  height: 1,
                }}
                onSave={handleSaveEdit}
                onCancel={handleCancelEdit}
              />
              <Button onClick={handleCancelEdit} className="mt-4">
                Cancel
              </Button>
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
                Are you sure you want to delete invoice{' '}
                <span className="font-bold text-white">
                  {invoiceToDelete.invoice}
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
