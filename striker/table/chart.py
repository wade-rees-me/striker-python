class ChartRow:
    def __init__(self):
        self.key = "--"
        self.value = [["---"] * 13 for _ in range(13)]  # 2, 3, ... A


class Chart:
    def __init__(self, name):
        self.rows = [ChartRow() for _ in range(21)]
        self.name = name
        self.nextRow = 0
        self.init_chart(name)

    def init_chart(self, name):
        self.name = name
        self.nextRow = 0
        for row in self.rows:
            row.key = "--"
            for i in range(13):
                row.value[i] = "---"

    def chart_get_row_count(self):
        return self.nextRow

    def chart_get_row(self, key):
        key = key.upper()
        for row in self.rows[:self.nextRow]:
            if row.key == key:
                return row
        return None

    def chart_insert(self, key, up, value):
        row = self.chart_get_row(key)
        if row is None:
            if self.nextRow >= len(self.rows):
                raise IndexError("Chart is full")
            row = self.rows[self.nextRow]
            self.nextRow += 1
            row.key = key.upper()
        row.value[up] = value.upper()

    def chart_get_value(self, key, up):
        row = self.chart_get_row(key)
        if row:
            return row.value[up]
        else:
            raise KeyError(f"Cannot find value in {self.name} for {key} vs {up}")

    def chart_get_value_by_total(self, total, up):
        key = str(total)
        return self.chart_get_value(key, up)

    def chart_print(self):
        print(self.name)
        print("--------2-----3-----4-----5-----6-----7-----8-----9-----T-----J-----Q-----K-----A---")
        for row in self.rows[:self.nextRow]:
            print(f"{row.key:2} :", end=" ")
            print(" ".join(f"{value:4}" for value in row.value))
        print("------------------------------------------------------------------------------------\n")

