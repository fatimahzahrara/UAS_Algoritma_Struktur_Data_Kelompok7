# =====================================================================
#  struktur_linear.py  |  Anggota 1
#  Implementasi Queue (FIFO) dan Stack (LIFO) secara mandiri.
# =====================================================================


# ===== QUEUE: array + pointer 'depan' (dequeue amortized O(1)) =====
class Queue:
    def __init__(self):
        self.items = []
        self.depan = 0

    def is_empty(self):
        return self.depan >= len(self.items)

    def size(self):
        return len(self.items) - self.depan

    def enqueue(self, data):
        self.items.append(data)

    def dequeue(self):
        if self.is_empty():
            return None
        data = self.items[self.depan]
        self.items[self.depan] = None       # bebaskan referensi
        self.depan += 1
        # rapikan memori bila banyak slot kosong
        if self.depan > 50 and self.depan * 2 > len(self.items):
            self.items = self.items[self.depan:]
            self.depan = 0
        return data

    def peek(self):
        return None if self.is_empty() else self.items[self.depan]

    def display(self):
        if self.is_empty():
            print("   (antrean pendaftaran kosong)")
            return
        for i in range(self.depan, len(self.items)):
            print(f"   {i - self.depan + 1}. {self.items[i]}")


# ===== STACK: berbasis linked list =====
class _SNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:
    def __init__(self):
        self.top = None
        self.jumlah = 0

    def is_empty(self):
        return self.top is None

    def push(self, data):
        node = _SNode(data)
        node.next = self.top
        self.top = node
        self.jumlah += 1

    def pop(self):
        if self.is_empty():
            return None
        node = self.top
        self.top = self.top.next
        self.jumlah -= 1
        return node.data

    def peek(self):
        return None if self.is_empty() else self.top.data

    def display(self):
        if self.is_empty():
            print("   (riwayat kosong)")
            return
        cur, i = self.top, 1
        while cur:
            print(f"   {i}. {cur.data}")
            cur, i = cur.next, i + 1
