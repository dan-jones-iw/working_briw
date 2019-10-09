import unittest
import unittest.mock
import source.round as rnd


class TestMethods(unittest.TestCase):
    # test initialisation of class
    def test_initialise(self):
        # Act
        test_round0 = rnd.Round()
        test_round1 = rnd.Round(1)
        test_round2 = rnd.Round(1, 1)

        # Assess
        self.assertIsInstance(test_round0, rnd.Round)
        self.assertEqual(test_round0.server_id, -1)
        self.assertEqual(test_round0.round_id, -1)
        self.assertEqual(test_round1.server_id, 1)
        self.assertEqual(test_round1.round_id, -1)
        self.assertEqual(test_round2.server_id, 1)
        self.assertEqual(test_round2.round_id, 1)

    def test_setters(self):
        # Arrange
        test_round = rnd.Round()

        # Act
        test_round.set_server_id(44)
        test_round.set_round_id(15)

        # Assess
        self.assertEqual(test_round.server_id, 44)
        self.assertEqual(test_round.round_id, 15)

    def test_delete(self):
        # Arrange
        test_round = rnd.Round(4, 5)

        # Act
        test_round.delete_round()

        # Assess
        self.assertEqual(test_round.server_id, -1)
        self.assertEqual(test_round.round_id, -1)

    @unittest.mock.patch('source.db.get_all_rounds', side_effect=[(), (1, 2), "pawsword"])
    def test_round_checker(self, operation):
        # Assess
        self.assertFalse(rnd.check_if_round_exists())
        self.assertTrue(rnd.check_if_round_exists())
        self.assertTrue(rnd.check_if_round_exists())

    @unittest.mock.patch('source.db.get_server_id_from_round_id', return_value=15)
    @unittest.mock.patch('source.db.get_max_round_id', return_value=6)
    @unittest.mock.patch('source.round.check_if_round_exists', return_value=True)
    def test_round_initialise_when_round_exists(self, op1, op2, db_get_server_id):
        # Arrange
        test_round = rnd.Round()

        # Act
        val = test_round.initialise_round()

        # Assert
        self.assertEqual(test_round.round_id, 6)
        db_get_server_id.assert_called_once()
        self.assertTrue(val)

    @unittest.mock.patch('source.db.new_round', return_value=1)
    @unittest.mock.patch('source.round.get_server_id_for_new_round', return_value=2)
    @unittest.mock.patch('source.db.get_number_of', return_value=4)
    @unittest.mock.patch('source.round.check_if_round_exists', return_value=False)
    def test_round_initialise_when_round_does_not_exist(self, op1, op2, op3, db_new_round):
        # Arrange
        test_round = rnd.Round()

        # Act
        val = test_round.initialise_round()

        # Assert
        self.assertEqual(test_round.server_id, 2)
        db_new_round.assert_called_once()
        self.assertTrue(val)

    @unittest.mock.patch('source.db.get_number_of', return_value=None)
    @unittest.mock.patch('source.round.check_if_round_exists', return_value=False)
    def test_round_initialise_when_no_people_exist(self, op1, op2):
        # Arrange
        test_round = rnd.Round()

        # Act
        val = test_round.initialise_round()

        # Assert
        self.assertEqual(test_round.server_id, -1)
        self.assertEqual(test_round.round_id, -1)


if __name__ == '__main__':
    unittest.main()
