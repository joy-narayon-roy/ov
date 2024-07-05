from worker import get_config, verify


def worker(id="ALL"):
    config = get_config(id)
    while True:
        reg = config.next()
        exist = verify(reg)
        if exist:
            config.this_valid_reg(reg)
            print(id, reg, "Exist")
        else:
            print(id, reg, "Not exist")
        # break


if __name__ == "__main__":
    try:
        worker("MAT")
    except KeyboardInterrupt:
        exit()
    except Exception as err:
        print(err)
