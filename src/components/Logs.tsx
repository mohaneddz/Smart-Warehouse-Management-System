import { useState, useEffect } from 'react';

function Logs(props: any) {
  const [color, setColor] = useState('green-400');

  useEffect(() => {
    if (props.in_out === '-') {
      setColor('red-500');
    } else {
      setColor('green-400');
    }
  }, [props.in_out]);

  return (
    <p className="text-white">
      <span className={`text-${color}`}>{props.in_out}</span> 20 items{' '}
      <span className="opacity-10 ml-">yesterday</span>
    </p>
  );
}

export default Logs;
