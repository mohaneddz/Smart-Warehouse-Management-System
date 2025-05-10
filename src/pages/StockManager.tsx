import Form from '../components/Addf.tsx';
import InventoryManager from '../components/Navigate.tsx';
import { useState } from 'react';
import RmEdTable from '@/components/RmEdTable.tsx';
import ManageTable from '@/components/ManageTable.tsx';
import { motion } from 'framer-motion';

function StockManager() {
  const [cardAction, setCardAction] = useState({
    Add: true,
    Remove: false,
    Manage: false,
  });

  // Callback to receive values from CarouselSpacing
  const handleCardAction = (Add: any, Remove: any, Manage: any) => {
    setCardAction({ Add, Remove, Manage });
  };
  return (
    <div className="flex flex-col items-center justify-start">
      <div className="min-w-min w-[90%]">
        <div
          className={`w-full mt-0 ${cardAction.Add ? 'mt-0' : ''} mb-5 flex justify-center`}
        >
          <InventoryManager onCardClick={handleCardAction} />
        </div>
        <div className="flex justify-center items-start w-full">
          {' '}
          {/* Changed items-center to items-start and added w-full */}
          <motion.div
            key={
              cardAction.Add ? 'add' : cardAction.Remove ? 'remove' : 'default'
            }
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 1.05 }}
            transition={{ duration: 0.4 }}
            className="w-full" // Ensure the content takes full width of its container
          >
            {cardAction.Add ? (
              <Form />
            ) : cardAction.Remove ? (
              <RmEdTable />
            ) : (
              <ManageTable />
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
}
export default StockManager;
