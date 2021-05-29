import unittest


class TestGeneral(unittest.TestCase):
    def test_crypt(self):
        """
            Test sid encrypt / decrypt function
        """
        from core.general.sidcrypt import SIDEncryption
        sid_crypt = SIDEncryption()
        string = 'its a big country'
        encrypted_string = sid_crypt.encrypt(string)
        self.assertEqual(string, sid_crypt.decrypt(encrypted_string))

    def test_downloadpath(self):
        """
            Test valid download path
        """
        from core.general.sidhelper import get_downloadpath
        fpath = get_downloadpath('admin')
        self.assertEqual(fpath, '/sid/external/documents/admin/')

    def test_filename(self):
        """
            Test valid download path
        """
        from core.general.sidhelper import generate_filename
        from datetime import date
        fpath = '/sid/external/documents/admin'
        fstartwith = 'test_'
        fendwith = '.csv'
        run_date = date.today()
        filemask = 'YYYYDDMM'
        filename = generate_filename(
            fpath,
            fstartwith,
            fendwith,
            run_date,
            filemask
        )
        ofile = fpath + '/' + fstartwith + run_date.strftime('%Y%d%m') + fendwith
        self.assertEqual(filename, ofile)
        """
            test DDMMYYYY
        """
        filemask = 'DDMMYYYY'
        filename = generate_filename(
            fpath,
            fstartwith,
            fendwith,
            run_date,
            filemask
        )
        ofile = fpath + '/' + fstartwith + run_date.strftime('%d%m%Y') + fendwith
        self.assertEqual(filename, ofile)

        """
            test MMDDYYYY
        """
        filemask = 'MMDDYYYY'
        filename = generate_filename(
            fpath,
            fstartwith,
            fendwith,
            run_date,
            filemask
        )
        ofile = fpath + '/' + fstartwith + run_date.strftime('%m%d%Y') + fendwith
        self.assertEqual(filename, ofile)

        """
            test YYYYMMDD
        """
        filemask = 'YYYYMMDD'
        filename = generate_filename(
            fpath,
            fstartwith,
            fendwith,
            run_date,
            filemask
        )
        ofile = fpath + '/' + fstartwith + run_date.strftime('%Y%d%m') + fendwith
        self.assertEqual(filename, ofile)

    def test_checkdateformat(self):
        """
            Test valid date
        """
        from core.general.sidhelper import check_dateformat
        from datetime import date
        date_part = check_dateformat('20-02-2021', 'DD-MM-YYYY')
        self.assertEqual(date(2021, 2, 20), date_part)

        date_part = check_dateformat('2021-02-20', 'YYYY-MM-DD')
        self.assertEqual(date(2021, 2, 20), date_part)

        date_part = check_dateformat('2021-20-02', 'YYYY-DD-MM')
        self.assertEqual(date(2021, 2, 20), date_part)

        date_part = check_dateformat('20/02/2021', 'DD/MM/YYYY')
        self.assertEqual(date(2021, 2, 20), date_part)

        date_part = check_dateformat('2021/02/20', 'YYYY/MM/DD')
        self.assertEqual(date(2021, 2, 20), date_part)

        date_part = check_dateformat('2021/20/02', 'YYYY/DD/MM')
        self.assertEqual(date(2021, 2, 20), date_part)
