/*in this page we navigate between three subpages:
 Add to enventory ,Manage enventory, take from enventory*/

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
    <div className="flex flex-col items-center justify-center min-h-screen">
      <div className="w-[50%] flex flex-col items-center justify-center">
        <div
          className={`w-full mt-20 ${cardAction.Add ? 'mt-43' : ''} mb-10 flex justify-center`}
        >
          <InventoryManager onCardClick={handleCardAction} />
        </div>
        <div className="flex justify-center items-center">
          <motion.div
            key={
              cardAction.Add ? 'add' : cardAction.Remove ? 'remove' : 'default'
            }
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 1.05 }}
            transition={{ duration: 0.4 }}
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
