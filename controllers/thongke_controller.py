from models.thongke import ThongKeModel

class ThongKeController:
    """Logic thống kê: tính si số, số đậu/rớt và điểm trung bình theo năm."""
    def __init__(self):
        self.model = ThongKeModel()

    def get_stats_year(self) -> list:

        rows = self.model.lay_all_diem()
        stats = {}
        for r in rows:
            year = r['nam']
            score = r['diem_tong_ket']
            if year not in stats:
                stats[year] = {'nam': year, 'si_so': 0, 'dau': 0, 'rot': 0, 'sum': 0.0}
            stats[year]['si_so'] += 1
            stats[year]['sum'] += score
            if score >= 5:
                stats[year]['dau'] += 1
            else:
                stats[year]['rot'] += 1
        result = []
        for y, v in sorted(stats.items()):
            diem_tb = round(v['sum'] / v['si_so'], 2) if v['si_so'] > 0 else 0.0
            result.append({'nam': y, 'si_so': v['si_so'], 'dau': v['dau'], 'rot': v['rot'], 'diem_tb': diem_tb})
        return result