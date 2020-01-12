# Homework 6
# Matt Mauer
# completed 11.19.19

from abc import ABC, ABCMeta, abstractmethod
from node import Node

class Queue(ABC):
    '''
      Queue is an Abstract Base class that represents an Queue interface
    ''' 
    @abstractmethod
    def enqueue(self, item):
        ''' 
        The enqueue method inserts an object into the queue
        ''' 
        pass  

    @abstractmethod 
    def dequeue(self):
        ''' 
        The dequeue method removes an object from the queue
        '''
        pass 

    @abstractmethod
    def __len__(self):
        '''   
           Returns the number of items in the queue. 
           It needs no parameters and returns an integer.
        ''' 
        pass 
    
    @abstractmethod
    def __bool__(self):
        '''   
           Returns whether the queue is empty or not. 
           it needs no parameters and returns a bool.
        ''' 
        pass 
    
    @abstractmethod
    def __iter__(self):
        '''   
           Returns an iterator of the objects inside the Queue 
        ''' 
        pass

class ListQueue(Queue):
    '''
    A ListQueue is an implementation of a Queue ADT that uses a Linked-List as its internal data strcuture. It must 
    use the notion of a linked-list that has Nodes as the elements in the list. Please refer back to the OrderedList 
    class from lecture.  
    '''
    # Initialize a queue with a  None value for rear and front
    # and 0 length index
    def __init__(self):
        self._front = None
        self._rear = None
        self._length = 0
    
    # If there are no Nodes in the queue yet, assign the item to rear and front,
    # if this isn't the queue isn't empty, add this item in the next node
    # on the rear, then update the rear.
    def enqueue(self, item):
        if self._length == 0:
            self._front = Node(item)
            self._rear = self._front
        else:
            self._rear.next = Node(item)
            self._rear = self._rear.next
        self._length += 1

    # Return None if queue is empty, otherwise
    # return the data of the next Node and reassign the the front
    def dequeue(self):
        if self._front == None:
            # OR RAISE ERROR????
            return None
        next_item = self._front.data
        self._front = self._front.next
        self._length -= 1
        return next_item
    
    # Return the length index
    def __len__(self):
        return self._length

    # Check wether there are are any Nodes in our queue
    def __bool__(self):
        if self._front == None:
            return False
        return True

    # Return a custom iterator class
    def __iter__(self):
        return ListQueueIterator(self._front)

class ListQueueIterator():
    # Initialize iterator with pointer on the first item in the queue
    def __init__(self, front_node):
        self._next_node = front_node
    
    # Return the data of the next node in the queue
    # Raise StopIteration error if there are no nodes left to return
    def __next__(self):
        if self._next_node == None:
            raise StopIteration
        next_item = self._next_node.data
        self._next_node = self._next_node.next
        return next_item
    
    # for formalities...
    def __iter__(self):
        return self

# A TEST
if __name__ == "__main__":
    q = ListQueue()
    print(bool(q))
    q.enqueue(4)
    print(q.dequeue())
    print(q.dequeue())
    q.enqueue('dog')
    q.enqueue(True)
    print(len(q))
    print(bool(q))
    q.enqueue(8.4)
    print(q.dequeue())
    print(q.dequeue())
    print(len(q))

